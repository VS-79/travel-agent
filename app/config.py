from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    openweather_api_key: str = ""
    tavily_api_key: str = ""
    faiss_index_path: str = "data/faiss_index"

    class Config:
        env_file = ".env"

settings = Settings()