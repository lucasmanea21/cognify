import tkinter as tk
from tkinter import messagebox, ttk
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
from datetime import datetime
from collections import deque
import threading

root = tk.Tk()
root.title("EEG Data Recorder")

tasks = ["Move Mouse Up", "Move Mouse Down", "Move Mouse Left", "Move Mouse Right", "Click"]

board = None
recording = False
data = []
sampling_rate = 250
window_size = sampling_rate
think_time = 10
rest_time = 5
current_phase = "thinking"
start_time = None
show_plot = False
trial_index = 0
saved_trials = []
data_buffer = deque(maxlen=sampling_rate * 10)  
data_lock = threading.Lock()
plot_fig, plot_ax = None, None

def load_board():
    global board
    if board is None:
        params = BrainFlowInputParams()
        board_id = BoardIds.SYNTHETIC_BOARD
        # params.serial_port = "/dev/cu.usbserial-D200PPDD"
        try:
            board = BoardShim(board_id, params)
            board.prepare_session()
            board.start_stream()
            print("Board loaded and streaming started.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to load the board: {e}")
            print(f"Failed to load the board: {e}")

def start_recording():
    global board, recording, data, start_time
    task = task_combo.get()
    if not task:
        messagebox.showwarning("Input Error", "Please select a task.")
        return
    
    if board is None:
        load_board()

    data = []
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    recording = True
    start_time = time.time()
    threading.Thread(target=update_phase, daemon=True).start()
    threading.Thread(target=record_task, daemon=True).start()

def update_phase():
    global current_phase, start_time
    while recording:
        elapsed_time = time.time() - start_time
        if current_phase == "thinking" and elapsed_time >= think_time:
            root.after(0, save_data)
            current_phase = "resting"
            start_time = time.time()
            root.after(0, lambda: phase_label.config(text="Resting... Please relax."))
        elif current_phase == "resting" and elapsed_time >= rest_time:
            current_phase = "thinking"
            start_time = time.time()
            root.after(0, lambda: phase_label.config(text="Recording... Please focus on the task."))
        root.after(0, update_animation)
        time.sleep(1)

def record_task():
    global board, recording, data, data_buffer
    while recording:
        try:
            board_data = board.get_board_data(num_samples=window_size)
            eeg_channels = [0, 1, 2, 3, 4, 5, 6, 7]

            for channel in eeg_channels:
                DataFilter.perform_bandpass(board_data[channel], sampling_rate, 7.0, 13.0, 4, FilterTypes.BUTTERWORTH, 0)

            with data_lock:
                data.append(board_data[eeg_channels, :])
                for sample in board_data[eeg_channels, :].T:
                    data_buffer.append(sample)

            if show_plot:
                root.after(0, update_plot)

            time.sleep(1 / sampling_rate)
        except Exception as e:
            messagebox.showerror("Recording Error", f"Failed to record data: {e}")
            print(f"Failed to record data: {e}")

def stop_recording():
    global board, recording, data
    recording = False
    board.stop_stream()
    board.release_session()
    root.after(0, save_data)
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def save_data():
    global data, trial_index, saved_trials
    task = task_combo.get()
    if not os.path.exists(f"../data/recorded/{task}"):
        os.makedirs(f"../data/recorded/{task}")

    with data_lock:
        flattened_data = np.hstack(data)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"../data/recorded/{task}/{task}_{timestamp}.csv"
        pd.DataFrame(flattened_data).to_csv(filename, index=False)
        trial_index += 1
        saved_trials.append(f"Trial #{trial_index}: saved as {task}_{timestamp}.csv")
        update_saved_trials()
        data.clear()

def update_saved_trials():
    saved_trials_text = "\n".join(saved_trials)
    status_label.config(text=f"Saved Trials:\n{saved_trials_text}")

def update_plot():
    global plot_fig, plot_ax
    if plot_fig is None:
        plt.ion()
        plot_fig, plot_ax = plt.subplots()
        plot_ax.set_title('Real-time EEG Data')
        plot_ax.set_xlabel('Time')
        plot_ax.set_ylabel('Amplitude')

    plot_ax.clear()
    data_array = np.array(data_buffer).T
    for channel in range(data_array.shape[0]):
        plot_ax.plot(data_array[channel], label=f"Channel {channel}")
    plot_ax.legend(loc="upper right")
    plot_fig.canvas.draw()
    plot_fig.canvas.flush_events()

def toggle_plot():
    global show_plot, plot_fig
    show_plot = not show_plot
    if show_plot:
        plt.ion()
        plot_button.config(text="Hide Plot")
    else:
        plt.close(plot_fig)
        plot_fig = None
        plot_button.config(text="Show Plot")

def update_animation():
    task = task_combo.get()
    x0, y0, x1, y1 = canvas.coords(mouse)
    if current_phase == "thinking":
        if task == "Move Mouse Up":
            if y0 > 0:
                canvas.move(mouse, 0, -animation_speed)
            else:
                canvas.coords(mouse, 190, 390, 210, 410)
        elif task == "Move Mouse Down":
            if y1 < 400:
                canvas.move(mouse, 0, animation_speed)
            else:
                canvas.coords(mouse, 190, -10, 210, 10)
        elif task == "Move Mouse Left":
            if x0 > 0:
                canvas.move(mouse, -animation_speed, 0)
            else:
                canvas.coords(mouse, 390, 190, 410, 210)
        elif task == "Move Mouse Right":
            if x1 < 400:
                canvas.move(mouse, animation_speed, 0)
            else:
                canvas.coords(mouse, -10, 190, 10, 210)
        elif task == "Click":
            canvas.itemconfig(mouse, fill="red")
            root.after(100, lambda: canvas.itemconfig(mouse, fill="black"))

animation_speed = 20
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
mouse = canvas.create_oval(190, 190, 210, 210, fill="black")

task_label = tk.Label(root, text="Select Task:")
task_label.pack()

task_combo = ttk.Combobox(root, values=tasks)
task_combo.pack()

start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.pack()

stop_button = tk.Button(root, text="Stop Recording", command=stop_recording, state=tk.DISABLED)
stop_button.pack()

plot_button = tk.Button(root, text="Show Plot", command=toggle_plot)
plot_button.pack()

phase_label = tk.Label(root, text="Thinking... Please focus on the task.")
phase_label.pack()

space_label = tk.Label(root, text="")
space_label.pack()

status_label = tk.Label(root, text="Saved Trials:\n")
status_label.pack()

root.mainloop()
