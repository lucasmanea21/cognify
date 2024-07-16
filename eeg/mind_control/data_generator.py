import numpy as np
import time
import threading
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from .plot_updater import simulate_prediction

board = None
running = False
data_lock = threading.Lock()

def load_board():
    global board
    params = BrainFlowInputParams()
    board_id = BoardIds.SYNTHETIC_BOARD
    # board_id = BoardIds.GANGLION_BOARD
    board = BoardShim(board_id, params)
    
    board.prepare_session()
    board.start_stream()

def generate_brainflow_data(y):
    global board, running
    while running:
        data = board.get_board_data()
        for i in range(data.shape[1]):
            # read first 4 channels
            new_data = data[1:5, i]  
            with data_lock:
                update_data(y, new_data)
            simulate_prediction()
        time.sleep(0.5)

def update_data(y, new_data):
    y[:] = np.roll(y, -1, axis=1)
    y[:, -1] = new_data
    print(f"New data: {new_data}")

def start_stream(y):
    global running
    running = True
    load_board()
    threading.Thread(target=generate_brainflow_data, args=(y,), daemon=True).start()

def stop_synthetic_stream():
    global running
    running = False

def get_current_data():
    global y
    with data_lock:
        return y.copy()
