import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file (located in backend directory)
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Digital Inheritor Backend"
    API_V1_STR: str = "/api/v1"

    # Neo4j Settings
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "fusu2023yzcm")

    # MySQL Settings
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = os.getenv("MYSQL_PORT", 3306)
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "inheritor_db")

    # LLM Settings - DeepSeek
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "sk-ef663e51e8224d99803c7fbc6f137a86")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # Image Generation Settings
    STABLE_DIFFUSION_API_URL: str = os.getenv("STABLE_DIFFUSION_API_URL", "http://localhost:7860")

    class Config:
        case_sensitive = True

settings = Settings()
