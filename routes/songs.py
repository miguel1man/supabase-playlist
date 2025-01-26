from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models.song import SongResponse
from utils.supabase_manager import SupabaseManager

router = APIRouter(
    prefix="/songs",
    tags=["songs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/ranking-by/{score_field}", response_model=List[SongResponse])
async def get_songs(score_field: str, order_field: str, select_fields: str):
    """
    # Obtiene canciones filtradas por un score mínimo
    # select_fields: title,score_2024_10,score_2024_q3,previous_score,youtube_url,id
    """
    try:
        client = SupabaseManager()
        songs = client.get_filtered_songs(
            score_field=score_field,
            order_field=order_field,
            select_fields=select_fields.split(","),
        )
        print(f"{songs=}")
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
        client = SupabaseManager()
        songs = client.get_songs_with_value(
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
        client = SupabaseManager()
        songs = client.get_songs_with_greater_or_equal(
            selected_field=selected_field,
            response_fields=response_fields.split(","),
            min_score=min_score,
        )
        print(f"Existen {len(songs)} canciones con un puntaje mayor a {min_score}")
        return songs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error get_songs: {str(e)}")


@router.get("/score-range/{selected_field}/", response_model=List[SongResponse])
async def get_songs_between(
    score_field: str,
    response_fields: str,
    score_greater_or_equal: float = 90,
    score_less_than: float = 100,
):
    """
    # Obtiene canciones filtradas por un score mínimo
    """
    try:
        client = SupabaseManager()
        songs = client.get_songs_by_score_range(
            score_field=score_field,
            response_fields=response_fields.split(","),
            score_greater_or_equal=score_greater_or_equal,
            score_less_than=score_less_than,
        )
        print(
            f"Existen {len(songs)} canciones con un puntaje mayor o igual a {score_greater_or_equal} y menor que {score_less_than}"
        )
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
        client = SupabaseManager()
        # Convertir empty_fields de string a lista
        empty_fields_list = empty_fields.split(",")

        # Procesar response_fields solo si se proporciona
        fields_list = response_fields.split(",") if response_fields else None

        songs = client.get_songs_with_zero_scores(
            empty_fields=empty_fields_list,
            order_field=order_field,
            response_fields=fields_list,
        )
        return songs
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching songs with zero scores: {str(e)}"
        )
