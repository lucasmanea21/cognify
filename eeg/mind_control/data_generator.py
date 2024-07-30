import numpy as np
import time
import threading
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from .plot_updater import simulate_prediction
from .record import save_eeg_data
import multiprocessing
from .visual_launcher import start_visualization

board = None
running = False
data_lock = threading.Lock()

def load_board():
    global board
    
    if board is None:
        params = BrainFlowInputParams()
        # board_id = BoardIds.SYNTHETIC_BOARD
        board_id = BoardIds.CYTON_BOARD
        params.serial_port = "/dev/cu.usbserial-D200PPDD"

        # params.serial_port = "COM3"

        board = BoardShim(board_id, params)
        
        board.prepare_session()
        board.start_stream()

def generate_brainflow_data(y, predicted_action, is_control):
    global board, running
    if board is None:
        load_board()
        
    while running:
        data = board.get_board_data()
        for i in range(data.shape[1]):
            # read first 4 channels
            new_data = data[1:5, i]  
            with data_lock:
                update_data(y, new_data)
            
            if is_control:
                simulate_prediction(predicted_action)
        time.sleep(0.5)

def update_data(y, new_data):
    # shift data to left
    y[:] = np.roll(y, -1, axis=1)
    y[:, -1] = new_data
    # print(f"New data: {new_data}")
    # print(f"Updated y: {y[:, -1]}")

def start_stream(y, predicted_action, is_control):
    global running
    running = True
    
    load_board()
    threading.Thread(target=generate_brainflow_data, args=(y, predicted_action, is_control), daemon=True).start()
    
    if is_control:
        multiprocessing.Process(target=start_visualization, args=(y, predicted_action)).start()

def record_focus_data(y, session_id, metrics_list, calculate_metrics):
    global running
    running = True
    
    def record():
        while running:
            data = get_current_data(y)
            
            metrics = calculate_metrics(data)
            metrics_list.append(metrics)

            save_eeg_data(session_id, data.tolist(), metrics_list)
            time.sleep(1)
    
    threading.Thread(target=generate_brainflow_data, args=(y, None, False), daemon=True).start()
    threading.Thread(target=record, daemon=True).start()

def stop_focus_data():
    global running
    running = False

def stop_synthetic_stream():
    global running
    running = False

def get_current_data(y):
    with data_lock:
        return y.copy()
