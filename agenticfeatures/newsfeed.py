import os
from dotenv import load_dotenv
import requests
import chromadb

class NewsFeed:

    _model_initilized = False
    BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()
    ENV_PATH = BASE_DIR / "config" / ".env"


    def __init__(self):

        """Check for Environment"""
        if not self.ENV_PATH.exists():
            raise ValueError("The environment does not exists")
        else:
             load_dotenv(self.ENV_PATH)
        
        """Load environment"""    
       
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.env = os.getenv("APP_ENV")
       
        """Initialize model """
        self.chromaClient = chromadb.CloudClient(
                api_key=os.get_env('CHROMA_CLOUD_API_KEY'),
                tenant=os.get_env('CHROMA_TENANT'),
                database=os.get_env('CHROMA_DB_NAME')
            )
            


