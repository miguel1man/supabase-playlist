from pydantic import BaseModel
from typing import Optional, Union


class SongResponse(BaseModel):
    """
    # Modelo Pydantic flexible para la respuesta de canciones
    """

    id: Optional[Union[str, int]] = None
    title: Optional[str] = None
    artist: Optional[str] = None
    youtube_url: Optional[str] = None
    previous_score: Optional[float] = None
    score_2024_10: Optional[float] = None
    score_2024_q3: Optional[float] = None
    score: Optional[float] = None

    class Config:
        from_attributes = True
