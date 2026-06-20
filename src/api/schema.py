# Import BaseModel from Pydantic
# BaseModel is used to define data schemas with validation rules
from pydantic import BaseModel


# Define a class that represents the structure of incoming API data
# LogInput inherits from BaseModel, so it gets validation + parsing features
class LogInput(BaseModel):

    # Each variable below is a field expected in the input JSON

    LineId: int = None
    # Field name: LineId
    # Type: int (integer)
    # Default value: None (optional field)

    Date: int = None
    # Date stored as integer (e.g., 81109)
    # Optional field

    Time: int = None
    # Time stored as integer (e.g., 203615)
    # Optional field

    Pid: int = None
    # Process ID as integer
    # Optional field

    Level: str
    # Required field (no default value)
    # Must be a string (e.g., "INFO", "ERROR")

    Component: str
    # Required field
    # Represents log source module or service name

    Content: str = None
    # Optional field
    # Full log message text

    EventId: str
    # Required field
    # Example: "E10", "E6"

    EventTemplate: str = None
    # Optional field
    # Template version of the log message (structured form)