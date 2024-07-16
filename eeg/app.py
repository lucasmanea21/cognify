from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import threading
import multiprocessing
from mind_control.data_generator import start_stream, stop_synthetic_stream, get_current_data
from mind_control.plot_updater import get_current_prediction
from mind_control.visual_launcher import start_visualization


app = Flask(__name__)
CORS(app)

# store data globally
y = np.zeros((4, 1000))

@app.route('/start_stream', methods=['POST'])
def start_stream_endpoint():
    threading.Thread(target=start_stream, args=(y,), daemon=True).start()
    
    multiprocessing.Process(target=start_visualization, args=(y,)).start()
    return jsonify({"message": "Stream started"}), 200

@app.route('/stop_stream', methods=['POST'])
def stop_stream_endpoint():
    stop_synthetic_stream()
    
    return jsonify({"message": "Stream stopped"}), 200

@app.route('/get_data', methods=['GET'])
def get_data():
    data = get_current_data()
    return jsonify({"data": data.tolist()}), 200

@app.route('/get_prediction', methods=['GET'])
def get_prediction():
    prediction = get_current_prediction()
    return jsonify({"prediction": prediction}), 200

if __name__ == '__main__':
    app.run(debug=True)
