import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = ""
    PROJECT_VERSION: str = "1.0.0"
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_URL: str = os.getenv("DB_URL")

settings=Settings()