from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Payment API"
    PROJECT_VERSION: str = "1.0.0"

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    PORT: int = 8000 

    @property
    def DB_URL(self):
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    SAFARICOM_BASE_URL: str
    CONSUMER_KEY: str
    SECRET: str
    PAYBILL: str
    PASSKEY: str
    CALLBACK_URL: str

    class Config:
        env_file = ".env"

settings = Settings()