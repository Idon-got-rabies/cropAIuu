from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm:str
    access_token_expire_minutes: int
    database_url: str
    weather_api_key: str
    ip_url:str
    weather_api_url:str
    base_url: str
    inflection_api_key: str
    inflection_api_url: str
    disease_api_url: str

    model_config = {
        "env_file": ".env"
    }

settings = Settings()



