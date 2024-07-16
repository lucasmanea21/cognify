import numpy as np

def extract_features(data):
    features = []
    
    for segment in data:
        feature = []
        for channel in segment:
            feature.append(np.mean(channel))
            feature.append(np.std(channel))
            feature.append(np.var(channel))
            feature.append(np.max(channel) - np.min(channel))
        features.append(feature)
    return np.array(features)
