import os


class GlobalConfig:
    # AWS
    DB_HOST: str = os.environ.get("DB_HOST", "http://dynamodb:8000")
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "test")
    AWS_REGION: str = os.environ.get("AWS_REGION", "eu-east-1")

    # Redis
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.environ.get("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.environ.get("REDIS_PASSWORD", "")

    # Email
    SMTP_SERVER: str = os.environ.get("SMTP_SERVER", "mailhog")
    SMTP_PORT: int = int(os.environ.get("SMTP_PORT", 1025))
    SMTP_SENDER: str = os.environ.get("SMTP_SENDER", "no-reply@example.com")


config = GlobalConfig()
