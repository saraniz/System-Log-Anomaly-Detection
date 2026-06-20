import pandas as pd
import joblib
from pathlib import Path

# BASE_DIR becomes the root project folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "feature.csv"
SAVE_MODEL_PATH = BASE_DIR / "models" / "isolation_model.pkl"


def load_model(path):
    """
    Load trained Isolation Forest model from disk
    """
    model = joblib.load(path)
    print("Model loaded successfully")
    return model


def load_data(path):
    """
    Load feature dataset or new incoming data
    """
    df = pd.read_csv(path)
    print("Data loaded:", df.shape)
    return df


def prepare_data(df):
    """
    Convert categorical columns into numeric features
    exactly same way as training phase
    """

    df = df.copy()

    # -------------------------
    # Remove prediction column if exists
    # -------------------------
    if "prediction" in df.columns:
        df = df.drop(columns=["prediction"])

    # -------------------------
    # Drop unnecessary text columns
    # -------------------------
    drop_cols = ["Content", "EventTemplate"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # -------------------------
    # Encode Level manually (IMPORTANT)
    # SAME as your training logic
    # -------------------------
    level_map = {
        "INFO": 0,
        "WARN": 1,
        "WARNING": 1,
        "ERROR": 2,
        "FATAL": 3
    }

    if "Level" in df.columns:
        df["Level"] = df["Level"].map(level_map)

        # Handle unknown values safely
        df["Level"] = df["Level"].fillna(0)

    # -------------------------
    # One-hot encode remaining categorical columns
    # -------------------------
    df = pd.get_dummies(df)

    return df


def predict(model, X):
    """
    Run anomaly detection
    """

    predictions = model.predict(X)

    # 1 = normal, -1 = anomaly
    X["prediction"] = predictions

    return X


if __name__ == "__main__":

    # 1. Load model
    model = load_model(SAVE_MODEL_PATH)

    # 2. Load features (simulate new data)
    df = load_data(DATA_PATH)

    # 3. Prepare input
    X = prepare_data(df)

    # 4. Predict anomalies
    result = predict(model, X)

    # 5. Show results
    print("\nPrediction summary:")
    print(result["prediction"].value_counts())

    print("\nSample output:")
    print(result.head())