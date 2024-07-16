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
def simulate_prediction():
    global predicted_action
    
    predicted_action = random.choice(predictions)
    print(f"Predicted action: {predicted_action}")
    perform_action(predicted_action)

def update_plot(frame, lines, prediction_text, y):
    for i, line in enumerate(lines):
        line.set_ydata(y[i])
        
    prediction_text.set_text(f"Prediction: {predicted_action}")
    return lines + [prediction_text]

def get_current_prediction():
    global predicted_action
    return predicted_action