from intasend import APIService
from dotenv import load_dotenv

load_dotenv()

import os 

token = os.getenv("API_TOKEN")
publishable_key = os.getenv("PUBLISHABLE_KEY")
service = APIService(token=token, publishable_key=publishable_key, test=True)

base_url=os.getenv("BASE_URL")


