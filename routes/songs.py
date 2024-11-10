from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models.song import SongResponse
from utils.supabase_manager import (
    get_filtered_songs,
    get_songs_with_greater_or_equal,
    get_songs_with_value,
    get_songs_with_zero_scores,
)

router = APIRouter(
    prefix="/songs",
    tags=["songs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/ranking-by/{score_field}", response_model=List[SongResponse])
async def get_songs(score_field: str, order_field: str, select_fields: str):
    """
    # Obtiene canciones filtradas por un score mínimo
    """
    try:
        songs = get_filtered_songs(
            score_field=score_field,
            order_field=order_field,
            select_fields=select_fields.split(","),
        )
        return songs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error get_songs: {str(e)}")


@router.get("/score-is/{selected_field}", response_model=List[SongResponse])
async def get_songs_with_score(
    selected_field: str, response_fields: str, selected_score: float
):
    """
    # Obtiene canciones filtradas por un valor
    """
    try:
        songs = get_songs_with_value(
            selected_field=selected_field,
            selected_score=selected_score,
            response_fields=response_fields.split(","),
        )
        print(f"Existen {len(songs)} canciones con un puntaje igual a {selected_score}")
        return songs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error get_songs: {str(e)}")


@router.get("/score-above/{selected_field}", response_model=List[SongResponse])
async def get_songs_min(
    selected_field: str, response_fields: str, min_score: float = 90
):
    """
    # Obtiene canciones filtradas por un score mínimo
    """
    try:
        songs = get_songs_with_greater_or_equal(
            selected_field=selected_field,
            response_fields=response_fields.split(","),
            min_score=min_score,
        )
        print(f"Existen {len(songs)} canciones con un puntaje mayor a {min_score}")
        return songs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error get_songs: {str(e)}")


@router.get("/zero-scores/", response_model=List[SongResponse])
async def get_zero_score_songs(
    empty_fields: str,  # Ahora recibe una cadena de campos separados por coma
    order_field: str,
    response_fields: Optional[str] = None,
):
    """
    # Obtiene canciones que tienen los campos especificados en null

    Args:
        empty_fields: Lista de campos a filtrar por null (separados por coma)
        order_field: Campo por el cual ordenar los resultados
        response_fields: Campos a incluir en la respuesta (opcional)
    """
    try:
        # Convertir empty_fields de string a lista
        empty_fields_list = empty_fields.split(",")

        # Procesar response_fields solo si se proporciona
        fields_list = response_fields.split(",") if response_fields else None

        songs = get_songs_with_zero_scores(
            empty_fields=empty_fields_list,
            order_field=order_field,
            response_fields=fields_list,
        )
        return songs
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching songs with zero scores: {str(e)}"
        )
