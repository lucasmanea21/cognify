import pyautogui

# todo: make transitions smoother
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
        pyautogui.move(10, 0)
        
        # pyautogui.click()

def get_smoothed_prediction():
    if len(prediction_buffer) == 0:
        return "none"
    
    # Apply smoothing to the buffer
    buffer_array = np.array([predictions.index(action) for action in prediction_buffer])
    smoothed_index = int(round(np.mean(buffer_array)))
    
    return predictions[smoothed_index]
