from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    openweather_api_key: str = ""
    tavily_api_key: str = ""
    serpapi_key: str = ""
    redis_url: str = ""
    faiss_index_path: str = "data/faiss_index"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()