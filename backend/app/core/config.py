"""
Application configuration management using Pydantic Settings.

All configuration is loaded from environment variables with sensible defaults.
Never hard-code secrets, credentials, or production URLs.
"""

from __future__ import annotations

from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    app_env: str = "development"
    debug: bool = False
    app_name: str = "CV Person Analytics"
    app_version: str = "1.0.0"
    secret_key: str = "change-this-to-a-random-secret-key-in-production"

    # --- Database ---
    database_url: str = "postgresql+asyncpg://cvuser:cvpassword@localhost:5432/cv_analytics"
    database_sync_url: str = "postgresql://cvuser:cvpassword@localhost:5432/cv_analytics"

    # --- Face Recognition ---
    face_match_threshold: float = 0.55
    face_model_name: str = "buffalo_l"
    face_embedding_dimension: int = 512
    face_min_quality_score: float = 0.5
    face_min_size: int = 80

    # --- Eye State Analysis ---
    eye_closed_threshold: float = 0.20
    eye_drowsy_duration_seconds: float = 1.5
    eye_sleep_duration_seconds: float = 3.0
    eye_smoothing_window: int = 5

    # --- Expression Analysis ---
    expression_confidence_threshold: float = 0.4
    expression_smoothing_window: int = 5

    # --- Detection Pipeline ---
    detection_fps: int = 15
    face_recognition_interval: int = 5
    hand_detection_interval: int = 2
    expression_detection_interval: int = 3
    max_persons: int = 10
    camera_source: str = "0"

    # --- Detection Event Storage ---
    event_batch_interval_seconds: int = 30
    event_retention_days: int = 30

    # --- File Upload ---
    max_upload_size_mb: int = 10
    allowed_image_extensions: str = "jpg,jpeg,png,webp"
    min_image_dimension: int = 100
    max_image_dimension: int = 4096

    # --- Server ---
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_url: str = "http://localhost:3000"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # --- Logging ---
    log_level: str = "INFO"
    log_format: str = "json"

    # --- Privacy ---
    retain_original_images: bool = True
    face_image_retention_days: int = 365
    auto_delete_inactive_persons_days: int = 0

    @property
    def allowed_extensions_list(self) -> List[str]:
        """Parse comma-separated extensions into a list."""
        return [ext.strip().lower() for ext in self.allowed_image_extensions.split(",")]

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def max_upload_size_bytes(self) -> int:
        """Convert MB to bytes."""
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def camera_source_parsed(self) -> int | str:
        """Parse camera source - integer for device index, string for URL."""
        try:
            return int(self.camera_source)
        except ValueError:
            return self.camera_source

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper_v = v.upper()
        if upper_v not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return upper_v


# Singleton settings instance
settings = Settings()
