import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "hdfs.csv"

# create reusable preprocessing pipeline
class LogPreprocessor:

    # constructor
    def __init__(self):
        
        # The self parameter is a reference to the current instance of the class.
        # Dictionary used to convert log levels into numeric values
        # This is important for ML models because they work with numbers, not text
        self.level_mapping = {
            "INFO": 0,      # Normal information logs
            "WARN": 1,      # Warning level (alternative spelling)
            "WARNING": 1,   # Same meaning as WARN → mapped to same value
            "ERROR": 2,     # Error level logs
            "FATAL": 3      # Critical system failure logs
        }

    def load_data(self, path: str):
        # Function to load CSV file from given file path

        df = pd.read_csv(path)  # Read CSV file into DataFrame

        print("Loaded data shape:", df.shape)  # Print rows and columns count
        return df  # Return loaded dataset

    def clean_columns(self, df: pd.DataFrame):
        """
        Remove unnecessary or redundant columns
        """

        # Check if column exists before dropping to avoid errors
        if "LineId" in df.columns:
            # LineId is usually just an index, not useful for ML
            df = df.drop(columns=["LineId"])

        return df  # Return cleaned dataset

    def encode_level(self, df: pd.DataFrame):
        """
        Convert categorical log levels into numeric format
        """

        # Map text values (INFO, ERROR, etc.) into numbers using dictionary
        df["Level"] = df["Level"].map(self.level_mapping)

        # Handle unknown or missing mappings (NaN values after mapping)
        # Replace them with 0 (default/neutral class)
        df["Level"] = df["Level"].fillna(0)

        return df  # Return updated dataset

    def process_time(self, df: pd.DataFrame):

        # Ensure string format
        df["Date"] = df["Date"].astype(str).str.zfill(6)
        df["Time"] = df["Time"].astype(str).str.zfill(6)

        # Convert Date (MMDDYY → YYYY-MM-DD)
        df["month"] = df["Date"].str[:2]
        df["day"] = df["Date"].str[2:4]
        df["year"] = df["Date"].str[4:6]

        # Assume 20xx century (important for dataset consistency)
        df["year"] = "20" + df["year"]

        # Convert Time (HHMMSS)
        df["hour"] = df["Time"].str[:2]
        df["minute"] = df["Time"].str[2:4]
        df["second"] = df["Time"].str[4:6]

        # Build proper datetime string
        df["datetime_str"] = (
            df["year"] + "-" +
            df["month"] + "-" +
            df["day"] + " " +
            df["hour"] + ":" +
            df["minute"] + ":" +
            df["second"]
        )

        # Now parsing WILL work
        df["datetime"] = pd.to_datetime(df["datetime_str"], errors="coerce")

        return df

    def final_cleanup(self, df: pd.DataFrame):
        """
        Remove temporary columns created during preprocessing
        """

        # List of intermediate columns that are no longer needed
        drop_cols = ["Date", "Time", "datetime_raw"]

        # Drop only columns that actually exist (prevents KeyError)
        df = df.drop(columns=[col for col in drop_cols if col in df.columns])

        return df  # Return final cleaned dataset

    def run(self, path: str):
        # Full preprocessing pipeline (step-by-step execution)

        df = self.load_data(path)        # Step 1: Load data
        df = self.clean_columns(df)     # Step 2: Remove unwanted columns
        df = self.encode_level(df)      # Step 3: Convert log level to numbers
        df = self.process_time(df)      # Step 4: Create datetime features
        df = self.final_cleanup(df)     # Step 5: Remove temporary columns

        print("\nPreprocessing complete")
        print("Final shape:", df.shape)
        print(df.head())  # Show first few rows for verification

        return df  # Return fully processed dataset


if __name__ == "__main__":
    # This block runs only when file is executed directly (not imported)

    path = DATA_PATH  # Dataset file path

    preprocessor = LogPreprocessor()  # Create object of preprocessing class

    processed_df = preprocessor.run(path)  # Run full pipeline