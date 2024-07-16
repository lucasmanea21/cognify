import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from .plot_updater import update_plot, init_plot

def start_visualization(y):
    fig, axs = plt.subplots(5, 1, figsize=(10, 10))  
    x = np.arange(0, 1000)
    lines, prediction_text = init_plot(axs, x, y)

    ani = animation.FuncAnimation(fig, update_plot, fargs=(lines, prediction_text, y), blit=True, interval=100)
    
    plt.show()
