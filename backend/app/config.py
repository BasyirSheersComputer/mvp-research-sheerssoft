"""
Application configuration loaded from environment variables.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql+asyncpg://sheerssoft:sheerssoft_dev_password@localhost:5432/sheerssoft"
    redis_url: str = "redis://localhost:6379/0"

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    # SendGrid
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = "reports@yourdomain.com"
    staff_notification_email: str = "reservations@vivatel.com.my"  # Default for pilot
    sendgrid_webhook_public_key: str = "" # Ed25519 public key for signature verification

    # WhatsApp
    whatsapp_verify_token: str = "sheerssoft_verify_token"
    whatsapp_api_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_app_secret: str = ""  # For webhook signature verification

    # Auth
    jwt_secret: str = "dev_jwt_secret_change_in_production"
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24
    
    # Admin Credentials
    admin_user: str = "admin"
    admin_password: str = "password123"

    # Environment
    environment: str = "development"
    allowed_origins: str = "http://localhost:3000"

    # Report scheduling
    daily_report_hour: int = 7
    daily_report_minute: int = 30
    timezone: str = "Asia/Kuala_Lumpur"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    def model_post_init(self, __context):
        if self.database_url.startswith("postgresql://"):
            self.database_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Cached singleton settings instance."""
    return Settings()
