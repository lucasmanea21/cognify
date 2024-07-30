import os
import pandas as pd
import numpy as np

def load_data(data_dir, segment_length=250):
    data = []
    labels = []
    actions = os.listdir(data_dir)
    
    for action in actions:
        action_dir = os.path.join(data_dir, action)
        if os.path.isdir(action_dir):
            
            for file in os.listdir(action_dir):
                file_path = os.path.join(action_dir, file)
                
                # print(f"file path: {file_path}")
                if os.path.isfile(file_path):
                    df = pd.read_csv(file_path)
                    segment = df.values
                    
                    if segment.shape[1] < segment_length:
                        padding = np.zeros((segment.shape[0], segment_length - segment.shape[1]))
                        segment = np.hstack((segment, padding))
                        
                    elif segment.shape[1] > segment_length:
                        segment = segment[:, :segment_length]
                    
                    data.append(segment)
                    labels.append(action)
    
    data = np.array(data)
    labels = np.array(labels)
    
    return data, labels
