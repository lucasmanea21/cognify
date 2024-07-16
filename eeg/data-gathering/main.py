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

def load_board():
    global board
    params = BrainFlowInputParams()
    board_id = BoardIds.SYNTHETIC_BOARD
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()

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
    update_phase()
    record_task()

def update_phase():
    global current_phase, start_time
    elapsed_time = time.time() - start_time
    if current_phase == "thinking" and elapsed_time >= think_time:
        save_data()
        current_phase = "resting"
        start_time = time.time()
        phase_label.config(text="Resting... Please relax.")
    elif current_phase == "resting" and elapsed_time >= rest_time:
        current_phase = "thinking"
        start_time = time.time()
        phase_label.config(text="Recording... Please focus on the task.")
    update_animation()
    root.after(1000, update_phase)

def record_task():
    global board, recording, data
    if recording:
        board_data = board.get_board_data(num_samples=window_size)
        eeg_channels = [0, 1, 2, 3]

        for channel in eeg_channels:
            DataFilter.perform_bandpass(board_data[channel], sampling_rate, 7.0, 13.0, 4, FilterTypes.BUTTERWORTH, 0)

        data.append(board_data[eeg_channels, :])

        if show_plot:
            update_plot(board_data[eeg_channels, :])

        root.after(1000, record_task)

def stop_recording():
    global board, recording, data
    recording = False
    board.stop_stream()
    board.release_session()
    save_data()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def save_data():
    global data, trial_index, saved_trials
    task = task_combo.get()
    if not os.path.exists(f"../data/recorded/{task}"):
        os.makedirs(f"../data/recorded/{task}")

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

def update_plot(board_data):
    plt.clf()
    for channel in range(board_data.shape[0]):
        plt.plot(board_data[channel], label=f"Channel {channel}")
    plt.legend(loc="upper right")
    plt.pause(0.001)

def toggle_plot():
    global show_plot
    show_plot = not show_plot
    if show_plot:
        plt.ion()
        fig, ax = plt.subplots()
        ax.set_title('Real-time EEG Data')
        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude')
        plot_button.config(text="Hide Plot")
    else:
        plt.close(fig)
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
