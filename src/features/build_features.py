# Import pandas library for working with tabular data (DataFrames)
import pandas as pd

# Import Path class for creating file paths that work across operating systems
from pathlib import Path


# __file__ = current Python file location
# resolve() = get absolute path
# parent.parent.parent = move up 3 directories
#
# Example:
# src/features/feature_engineering.py
#        ↑
#        ↑ parent
# src
#        ↑ parent
# project_root
#
# BASE_DIR becomes the root project folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Build path to the input dataset
#
# Equivalent to:
# data/raw/hdfs.csv
#
# Path automatically uses correct separators for Windows/Linux/Mac
DATA_PATH = BASE_DIR / "data" / "raw" / "hdfs.csv"


# Build path where processed features will be saved
#
# Equivalent to:
# data/processed/feature.csv
SAVED_PATH = BASE_DIR / "data" / "processed" / "feature.csv"


def build_features(df):
    """
    Convert categorical log information into numerical features
    that can be used by Isolation Forest.

    Input:
        df -> preprocessed log dataset

    Output:
        feature_df -> machine-learning-ready dataset
    """

    # Create a copy of the DataFrame
    #
    # This prevents accidental modification of the original dataset
    feature_df = df.copy()

    # EventId contains text categories:
    #
    # E1
    # E2
    # E3
    #
    # Machine learning algorithms cannot directly understand text,
    # so we convert categories into numeric columns using
    # One-Hot Encoding.
    #
    # Example:
    #
    # EventId
    # E1
    # E2
    # E3
    #
    # becomes
    #
    # event_E1 event_E2 event_E3
    #    1         0         0
    #    0         1         0
    #    0         0         1
    #
    # prefix="event" adds "event_" before each generated column
    # get_dummies() is pandas function that is used for the one hot encoding.conver categorical values into numerical values
    # prefix add 'event' before the each generated column name
    event_features = pd.get_dummies(
        feature_df["EventId"],
        prefix="event"
    )

    # Component is also categorical text:
    #
    # dfs.DataNode
    # dfs.NameNode
    # dfs.FSNamesystem
    #
    # Convert each unique component into separate binary columns
    component_features = pd.get_dummies(
        feature_df["Component"],
        prefix="component"
    )

    # Combine original dataframe with newly generated
    # event and component feature columns
    #
    # axis=1 means:
    # add columns horizontally
    #
    # axis=0 would add rows vertically
    feature_df = pd.concat(
        [
            feature_df,
            event_features,
            component_features
        ],
        axis=1
    )

    # Isolation Forest requires numerical input.
    #
    # These columns contain text and are not directly usable:
    columns_to_drop = [
        "Content",        # Full log message
        "EventTemplate",  # Log template text
        "EventId",        # Replaced by one-hot encoded columns
        "Component"       # Replaced by one-hot encoded columns
    ]

    # Drop unwanted columns
    #
    # inplace=True means modify feature_df directly
    # without creating a new DataFrame
    feature_df.drop(
        columns=columns_to_drop,
        inplace=True
    )

    # Return final feature dataset
    return feature_df


# This block runs only when the file is executed directly
#
# It does NOT run if this file is imported into another script
if __name__ == "__main__":

    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(
        DATA_PATH
    )


    # Convert raw/preprocessed logs into ML features
    features = build_features(df)

    # Show number of rows and columns
    print("\nFeature Dataset Shape:")
    print(features.shape)

    # Show all column names
    print("\nColumns:")
    print(features.columns)

    # Show first 5 rows
    print("\nSample:")
    print(features.head())

    # SAVED_PATH.parent returns:
    #
    # data/processed
    #
    # mkdir() creates folder
    #
    # parents=True:
    # create missing parent folders automatically
    #
    # exist_ok=True:
    # do not raise error if folder already exists
    SAVED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save final feature dataset as CSV
    #
    # index=False prevents pandas from saving
    # row numbers as an extra column
    features.to_csv(
        SAVED_PATH,
        index=False
    )

    # Confirmation message
    print("\nFeature file saved successfully.")