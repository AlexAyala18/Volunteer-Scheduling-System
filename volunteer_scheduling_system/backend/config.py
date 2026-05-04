import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings loaded from environment variables."""

    # MongoDB connection string - default to a local MongoDB instance if not specified
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/volunteer_db").strip()
    
    @classmethod
    def validate(cls):
        """
        Ensure essential configuration variables are set.
        """
        required_vars = ["MONGO_URI"]
        for var in required_vars:
            if not getattr(cls, var):
                raise ValueError(f"Error: {var} is missing from environment variables.")

# Create an instance of the Config class that can be imported elsewhere
config = Config()
