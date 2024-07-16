import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from loader import load_data
from features import extract_features
from utils import standardize_data, train_model, evaluate_model, save_model

data_dir = '../data/recorded'
data, labels = load_data(data_dir)

print(f"shape: {data.shape}")
print(f"labels: {np.unique(labels, return_counts=True)}")

plt.plot(data[0][0])
plt.title(f"Sample Data - {labels[0]}")
plt.show()

features = extract_features(data)
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

X_train, X_test, scaler = standardize_data(X_train, X_test)

clf = train_model(X_train, y_train)

accuracy = evaluate_model(clf, X_test, y_test)
print(f'Model accuracy: {accuracy * 100:.2f}%')

save_model(clf, scaler, 'random_forest_model.pkl', 'scaler.pkl')
