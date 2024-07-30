import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading
import time
import argparse
import random
import pyautogui
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

fig, axs = plt.subplots(5, 1, figsize=(10, 10))  # Add an extra subplot
x = np.arange(0, 1000)
y = np.zeros((4, 1000))
lines = [ax.plot(x, y[i])[0] for i, ax in enumerate(axs[:4])]
for ax in axs[:4]:
    ax.set_ylim([-2000, 2000])

axs[4].axis('off')  # Turn off the axis for the text display
prediction_text = axs[4].text(0.5, 0.5, "Prediction: None", fontsize=14, verticalalignment='center', horizontalalignment='center')

predictions = ["mouse up", "mouse down", "mouse left", "mouse right", "click"]
predicted_action = "None"

def generate_random_synthetic_data():
    while True:
        new_data = np.random.randn(4) * 100  # Four channels of random data
        update_data(new_data)
        simulate_prediction()
        time.sleep(0.5)

def generate_brainflow_synthetic_data():
    global board
    while True:
        data = board.get_board_data()
        for i in range(data.shape[1]):
            new_data = data[1:5, i]  # Read first four channels
            update_data(new_data)
            simulate_prediction()
        time.sleep(0.5)

def update_data(new_data):
    global y
    y = np.roll(y, -1, axis=1)
    y[:, -1] = new_data
    print(f"New data: {new_data}")

def simulate_prediction():
    global predicted_action
    predicted_action = random.choice(predictions)
    print(f"Predicted action: {predicted_action}")
    perform_action(predicted_action)

def perform_action(action):
    if action == "mouse up":
        pyautogui.move(0, -10)
    elif action == "mouse down":
        pyautogui.move(0, 10)
    elif action == "mouse left":
        pyautogui.move(-10, 0)
    elif action == "mouse right":
        pyautogui.move(10, 0)
    elif action == "click":
        pyautogui.click()

def update_plot(frame):
    for i, line in enumerate(lines):
        line.set_ydata(y[i])
    prediction_text.set_text(f"Prediction: {predicted_action}")
    return lines + [prediction_text]

def start_synthetic_stream(use_brainflow=False):
    if use_brainflow:
        threading.Thread(target=generate_brainflow_synthetic_data, daemon=True).start()
    else:
        threading.Thread(target=generate_random_synthetic_data, daemon=True).start()

parser = argparse.ArgumentParser(description="Real-time EEG data visualization.")
parser.add_argument('--use-brainflow', action='store_true', help="Use BrainFlow synthetic data stream.")
args = parser.parse_args()

start_synthetic_stream(use_brainflow=args.use_brainflow)

ani = animation.FuncAnimation(fig, update_plot, blit=True, interval=100)

plt.show()
