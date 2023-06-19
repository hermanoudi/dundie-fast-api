"""Database Connection"""
from sqlmodel import create_engine
from .config import settings

engine = create_engine(
    settings.db.uri,    # pytright: ignore
    echo=settings.db.echo,  # pytright: ignore
    connect_args=settings.db.connect_args,  # pytright: ignore
)
