import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from .plot_updater import update_plot, init_plot

def start_visualization(y, predicted_action):
    fig, axs = plt.subplots(5, 1, figsize=(10, 10))  
    x = np.arange(0, 1000)
    y_array = np.array(y).reshape((4, 1000))
    lines, prediction_text = init_plot(axs, x, y_array)

    def update_plot_wrapper(frame):
        return update_plot(frame, lines, prediction_text, y_array, predicted_action)

    ani = animation.FuncAnimation(fig, update_plot_wrapper, blit=True, interval=100)
    
    plt.show()