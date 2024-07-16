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
        pyautogui.click()
