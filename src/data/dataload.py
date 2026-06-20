# 1. first step - understand the data
import pandas as pd
from pathlib import Path

# __file__ = current Python script file path
# resolve() = converts it into absolute path (removes ambiguity like ../)
# parent.parent = moves up two directories → usually project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "hdfs.csv"

def load_data():

    print("DATA PATH:", DATA_PATH)

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"File not found at: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    print("Data is loaded...")

    print("Shape: ",df.shape)
    print("Columns: ", df.columns)
    print("Sample data: ", df.head())

    return df

# This block runs only when this file is executed directly
# (not when imported into another Python file)
if __name__ == "__main__":
    df = load_data()  # Call function and store returned DataFrame