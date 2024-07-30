import numpy as np
import random
from .action_performer import perform_action

predictions = ["mouse up", "mouse down", "mouse left", "mouse right", "click"]
predicted_action = "none"


def init_plot(axs, x, y):
    lines = [ax.plot(x, y[i])[0] for i, ax in enumerate(axs[:4])]
    
    for ax in axs[:4]:
        ax.set_ylim([-2000, 2000])
    axs[4].axis('off') 
    
    prediction_text = axs[4].text(0.5, 0.5, "Prediction: none", fontsize=14, verticalalignment='center', horizontalalignment='center')
    return lines, prediction_text

# simulates model predictions
# todo: replace with actual model
def simulate_prediction(predicted_action):
    action = random.choice(predictions)
    print(f"Predicted action: {action}")
    predicted_action[0] = action  
    
    perform_action(action)
    
def get_smoothed_prediction():
    if not prediction_buffer:
        return "none"
    
    # use the most frequent prediction in the buffer
    smoothed_action = max(set(prediction_buffer), key=prediction_buffer.count)
    return smoothed_action


def update_plot(frame, lines, prediction_text, y, predicted_action):
    for i, line in enumerate(lines):
        line.set_ydata(y[i])
    prediction_text.set_text(f"Prediction: {predicted_action[0]}") 
    
    return lines + [prediction_text]

def get_current_prediction(predicted_action):
    return predicted_action[0]