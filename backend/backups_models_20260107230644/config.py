
# app/core/config.py
import json
import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    """
    يسمح بقيم:
    - نص مفصول بفواصل: "http://a.com, http://b.com"
    - قائمة JSON كنص: '["http://a.com","http://b.com"]'
    - قائمة Python: ["http://a.com", "http://b.com"]
    - نص مفرد: "http://a.com"
    """
    if v is None:
        return []

    if isinstance(v, str):
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [str(i).strip().rstrip("/") for i in parsed if str(i).strip()]
                return v
            except json.JSONDecodeError:
                pass
        return [i.strip().rstrip("/") for i in v.split(",") if i.strip()]

    if isinstance(v, (list, tuple)):
        return [str(i).strip().rstrip("/") for i in v if str(i).strip()]

    if isinstance(v, (AnyUrl,)):
        return [str(v).rstrip("/")]

    raise ValueError(f"Invalid BACKEND_CORS_ORIGINS value: {v!r}")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",             # ضع .env بجانب الكود (داخل WORKDIR)
        env_ignore_empty=True,
        extra="ignore",
    )

    # عام
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    # CORS
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        origins: list[str] = []
        if isinstance(self.BACKEND_CORS_ORIGINS, list):
            origins.extend([str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS])
        elif isinstance(self.BACKEND_CORS_ORIGINS, str):
            origins.append(self.BACKEND_CORS_ORIGINS.rstrip("/"))
        if self.FRONTEND_HOST:
            origins.append(self.FRONTEND_HOST.rstrip("/"))
        return sorted(set(origins))

    # تعريف المشروع وقاعدة البيانات
    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None  # بدّل إلى AnyUrl إن أردت مرونة أكبر

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    # Optional override to use a different SQLAlchemy URL (useful for local tests)
    DB_URL_OVERRIDE: str | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Return a normalized SQLAlchemy database URI.

        Construct the URI explicitly to avoid subtle double-slash
        behavior coming from PostgresDsn.build that can result in
        a DB name like "/btec_db" being used by the DB driver.
        """
        # Allow overriding the DB URL via env var for tests or local overrides
        if self.DB_URL_OVERRIDE:
            return str(self.DB_URL_OVERRIDE)

        db_name = str(self.POSTGRES_DB).lstrip("/")
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{db_name}"
        )

    # إعدادات البريد الإلكتروني
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    # مستخدم اختباري + أول سوبر يوزر
    EMAIL_TEST_USER: EmailStr = "test@example.com"
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        # لا حاجة لفحص SECRET_KEY لأنه يولد عشوائيًا
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret("FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD)
        return self


settings = Settings()  #
