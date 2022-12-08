import os
from typing import (
    Optional,
    Dict,
    Any,
    Union,
    List,
)

from pydantic import (
    BaseSettings,
    PostgresDsn,
    validator,
    EmailStr,
    AnyHttpUrl,
)


class Settings(BaseSettings):

    API_VERSION: str = "v1"
    API_PREFIX: str = f"/api/{API_VERSION}"

    PROJECT_NAME: str
    SERVER_HOST: str

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 180

    DB_SCHEME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: Union[int, str]
    DB_NAME: str

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 2525
    SMTP_HOST: Optional[str] = "smtp.mailtrap.io"
    SMTP_USER: Optional[str] = "username"
    SMTP_PASSWORD: Optional[str] = "password"

    EMAILS_ENABLED: bool = False
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAILS_TEMPLATES_DIR: str = "/app/emails/templates"
    EMAILS_RESET_TOKEN_EXPIRE_HOURS: int = 2

    DB_POOL_SIZE: int = 83
    WEB_CONCURRENCY: int = 9
    POOL_SIZE: int = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

    ASYNC_DB_URI: Optional[str]

    @validator("ASYNC_DB_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme=values.get("DB_SCHEME"),
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=str(values.get("DB_PORT")),
            path=f"/{values.get('DB_NAME') or ''}",
        )

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    SECRET_KEY: str
    BACKEND_CORS_ORIGINS: Union[List[str], List[AnyHttpUrl]]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("~/.env")


settings = Settings()
