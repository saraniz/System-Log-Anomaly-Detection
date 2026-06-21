import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest
import joblib

# BASE_DIR becomes the root project folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "feature.csv"
SAVE_MODEL_PATH = BASE_DIR / "models" / "isolation_model.pkl"

#load the data
def load_data(DATA_PATH):

    df = pd.read_csv(DATA_PATH)
    print("DATA: ", df.head())

    return df

#prepare model
def prepare_data(df):

    X = df.copy()

    # Drop known useless columns
    drop_cols = ["Content", "EventTemplate"]
    X = X.drop(columns=[c for c in drop_cols if c in X.columns])

    # Encode Level
    level_map = {
        "INFO": 0,
        "WARN": 1,
        "WARNING": 1,
        "ERROR": 2,
        "FATAL": 3
    }

    if "Level" in X.columns:
        X["Level"] = X["Level"].map(level_map).fillna(0)

    # Convert remaining categorical columns using one-hot encoding
    X = pd.get_dummies(X)

    training_columns = X.columns
    joblib.dump(training_columns, SAVE_MODEL_PATH.parent / "columns.pkl")

    return X

def train_model(X):
    """
    Train Isolation Forest model for anomaly detection
    """

    model = IsolationForest(

        # isolation forest does not know what anomaly_rate is automatically.so we have to guide it using giving expect rate
        # “Set the sensitivity of anomaly detection”
        #     higher value → more anomalies detected
        #     lower value → fewer anomalies detected
        # expected proportion of anomalies in dataset
        contamination=0.1,

        # ensures reproducibility
        random_state=42
    )

    # Fit model on data (learn normal patterns)
    model.fit(X)

    print("Model training completed")

    return model


def evaluate_model(model, X):
    """
    Run predictions on training data to inspect results
    """

    predictions = model.predict(X)

    # 1 = normal, -1 = anomaly
    X["prediction"] = predictions

    print("\nPrediction distribution:")
    print(X["prediction"].value_counts())

    return X


def save_model(model, path):
    """
    Save trained model to disk for later API use
    """

    joblib.dump(model, path)
    print(f"Model saved at: {path}")


if __name__ == "__main__":

    # 1. Load feature dataset
    df = load_data(DATA_PATH)

    # 2. Prepare ML input
    X = prepare_data(df)

    # 3. Train model
    model = train_model(X)

    # 4. Evaluate quickly
    result_df = evaluate_model(model, X)

    # 5. Save model
    save_model(model, SAVE_MODEL_PATH)

    print("Shape:", X.shape)
    print("Missing values:", X.isna().sum().sum())
    print(X.describe())

