from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class SongResponse(BaseModel):
    """
    # Modelo Pydantic flexible para la respuesta de canciones
    """

    id: Optional[UUID] = None
    title: Optional[str] = None
    artist: Optional[str] = None
    youtube_url: Optional[str] = None
    previous_score: Optional[float] = None
    score_2024_10: Optional[float] = None
    score_2024_q3: Optional[float] = None
    score_2025_01: Optional[float] = None
    score: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
