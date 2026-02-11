import os
from dotenv import load_dotenv
import requests
class NewsFeed{

    _model_initilized = False
    BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()
    ENV_PATH = BASE_DIR / "config" / ".env"


    def __init__(self):

        """Check for Environment"""
        if not self.ENV_PATH.exists():
            raise ValueError "The environment does not exists"
        """Load environment"""    
        load_dotenv(self.ENV_PATH)
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
       
       """Initialize model """
        self.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            api_key= self.api_key
        )
        

}