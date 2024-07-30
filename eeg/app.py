from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import time
import threading
import multiprocessing
from mind_control.data_generator import start_stream, record_focus_data,stop_focus_data, stop_synthetic_stream, get_current_data, load_board, generate_brainflow_data
from mind_control.plot_updater import get_current_prediction
from mind_control.visual_launcher import start_visualization
from mind_control.record import start_focus_session, save_eeg_data
from flask_socketio import SocketIO, emit
from analysis.main import calculate_metrics



app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

y = np.zeros((4, 1000))
predicted_action = ["None"]
metrics_list = []

@app.route('/connect_board', methods=['POST'])
def connect_board_endpoint():
    load_board()
    return jsonify({"message": "Board connected"}), 200

@app.route('/start_stream', methods=['POST'])
def start_stream_endpoint():
    threading.Thread(target=start_stream, args=(y, predicted_action, True), daemon=True).start()
    
    return jsonify({"message": "Stream started"}), 200


@app.route('/stop_stream', methods=['POST'])
def stop_stream_endpoint():
    stop_synthetic_stream()
    
    return jsonify({"message": "Stream stopped"}), 200

@app.route('/start_focus', methods=['POST'])
def start_focus_endpoint():
    global current_session_id, recording
    
    current_session_id = start_focus_session()
    recording = True
    threading.Thread(target=record_focus_data, args=(y, current_session_id, metrics_list, calculate_metrics), daemon=True).start()
    
    return jsonify({"message": "Focus session started", "session_id": current_session_id}), 200

@app.route('/stop_focus', methods=['POST'])
def stop_focus_endpoint():
    threading.Thread(target=stop_focus_data, daemon=True).start()

    
    return jsonify({"message": "Focus session stopped"}), 200


@app.route('/get_data', methods=['GET'])
def get_data():
    data = get_current_data()
    
    return jsonify({"data": data.tolist()}), 200

@app.route('/get_prediction', methods=['GET'])
def get_prediction():
    prediction = get_current_prediction(predicted_action)
    
    return jsonify({"prediction": prediction}), 200

# streaming to client

@socketio.on('connect')
def handle_connect():
    emit('response', {'message': 'Connected to WebSocket'})

@socketio.on('start_data_stream')
def start_data_stream(sid = None):
    
    print("Starting data stream")
    threading.Thread(target=start_stream, args=(y, predicted_action, False), daemon=True).start()
    
    def stream_data():
        while True:
            data = get_current_data(y)
            metrics = calculate_metrics(data)

            socketio.emit('eeg_data', {'data': data.tolist(), 'metrics': metrics})
            time.sleep(0.04)  

    threading.Thread(target=stream_data,  daemon=True).start()

# helper functions



if __name__ == '__main__':
    app.run(debug=True)
