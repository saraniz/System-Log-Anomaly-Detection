from fastapi import FastAPI
import pandas as pd
import joblib
from pathlib import Path

from src.model.predict import prepare_data
from src.api.schema import LogInput

# BASE_DIR becomes the root project folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "feature.csv"
SAVE_MODEL_PATH = BASE_DIR / "models" / "isolation_model.pkl"

app = FastAPI(title="Log Anomaly Detection API")

# -----------------------------
# Load trained model once
# -----------------------------
model = joblib.load(SAVE_MODEL_PATH)


@app.get("/")
def home():
    return {"message": "Anomaly Detection API is running"}


@app.post("/predict")
def predict(log: LogInput):
    """
    Receive log data → convert → predict anomaly
    """

    # Convert input to dataframe
    df = pd.DataFrame([log.dict()])

    # Preprocess (VERY IMPORTANT - same as training)
    X = prepare_data(df)

    # Ensure same columns as training
    X = X.reindex(columns=model.feature_names_in_, fill_value=0)

    # Prediction
    prediction = model.predict(X)[0]

    # Convert result
    result = "NORMAL" if prediction == 1 else "ANOMALY"

    return {
        "prediction": result
    }