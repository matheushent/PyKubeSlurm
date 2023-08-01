from pathlib import Path

from pydantic import Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """General settings class for the entire application."""
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    CRD_GROUP: str = Field("mhtosta.engineering", description="Custom Resource Definition group.")
    CRD_VERSION: str = Field("v1alpha1", description="Custom Resource Definition version.")
    JOB_CRD_PLURAL: str = Field("slurmjobs", description="Custom Resource Definition plural name for jobs.")
    DEBUG_LEVEL: str = Field("DEBUG", description=(
        "Log levels allowed. Must be one of those defined "
        "on https://docs.python.org/3/library/logging.html#logging-levels"
    ))
    KUBE_CONFIG: str = Field("~/.kube/config", description="Path to the Kubernetes config file. Ignored if the app is run in cluster.")
    KUBE_CONTEXT: str = Field("minikube", description="Name of the Kubernetes context to use. Ignored if the app is run in cluster.")
    NAMESPACE: str = Field("default", description="Namespace to use for the application. Ignored if WATCH_ALL is set True.")
    WATCH_ALL: bool = Field(False, description="If True, the application will watch all namespaces.")
    EVENT_LISTENER_TIMEOUT: int = Field(10, description="Timeout in seconds for the event listener.")
    SLURMRESTD_USER_TOKEN: str = Field("ubuntu", description="Call the Slurmrestd endpoints on behalf of this user.")
    SLURMRESTD_JWT_KEY_PATH: Path = Field(..., description=(
        "Path of the JWT key file to use for issuing JWT tokens on behalf of the SLURMRESTD_USER_TOKEN user."
    ))
    CACHE_DIR: Path = Field("~/.pykubeslurm/cache", description="Cache directory for the entire app.")
    SLURMRESTD_TIMEOUT: float | None = Field(10, description="Timeout in seconds for the Slurmrestd endpoint. If None, timeout is disabled.")
    SLURMRESTD_ENDPOINT: str = Field("http://localhost:6820", description="The Slurmrestd endpoint.")
    SLURMRESTD_EXP_TIME_IN_SECONDS: float = Field(24 * 60 * 60, description="The Slurmrestd JWT token will expire after this many seconds.")

    @field_validator("DEBUG_LEVEL")
    def validate_debug_level(cls, v: str, info: FieldValidationInfo) -> str:
        """Validate that the DEBUG_LEVEL is one of those allowed."""
        if v not in ["NOTSET", "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
            raise ValueError(f"Invalid DEBUG_LEVEL: {v}")
        return v


SETTINGS = Settings()
