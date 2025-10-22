from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):   
    # Aplicação
    APP_NAME: str
    APP_VERSION: str
    ENVIRONMENT: str
    DEBUG: bool
    
    # Logging
    LOG_LEVEL: str 
    LOG_TO_FILE: bool 
    LOG_TO_CONSOLE: bool 
    LOG_JSON_FORMAT: bool
    
    # AWS Credentials
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: Optional[str] = None 
    
    # GCP Credentials
    GCP_PROJECT_ID: Optional[str] = None
    GCP_CREDENTIALS_PATH: Optional[str] = None
    
    # API Settings
    API_HOST: str
    API_PORT: int
    API_PREFIX: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Instância global das configurações
settings = get_settings()