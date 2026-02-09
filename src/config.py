"""Configuration du projet ETL."""
import os


class Config:
    """Configuration centralisee via variables d’environnement."""

    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = int(os.environ.get("DB_PORT", 3306))
    DB_NAME = os.environ.get("DB_NAME", "gametracker_db")
    DB_USER = os.environ.get("DB_USER", "gametracker")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "tracker")
    DATA_DIR = os.environ.get("DATA_DIR", "/app/data/raw")