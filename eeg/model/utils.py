from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def standardize_data(X_train, X_test):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test, scaler

def train_model(X_train, y_train):
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    return clf


def evaluate_model(clf, X_test, y_test):
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return accuracy

def save_model(clf, scaler, model_path='random_forest_model.pkl', scaler_path='scaler.pkl'):
    joblib.dump(clf, model_path)
    joblib.dump(scaler, scaler_path)
    
    

def load_model(model_path='random_forest_model.pkl', scaler_path='scaler.pkl'):
    clf = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return clf, scaler
