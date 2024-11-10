import os
from typing import List
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path
from models.song import SongResponse


def get_project_root() -> Path:
    """
    # Obtiene la ruta raíz del proyecto
    """
    return Path(__file__).parent.parent


def load_env_vars():
    """
    # Carga las variables de entorno desde el archivo .env en la raíz
    """
    env_path = get_project_root() / ".env"
    load_dotenv(dotenv_path=env_path)


class SupabaseManager:
    """
    # Manejador de conexiones y consultas a Supabase
    """

    def __init__(self):
        load_env_vars()
        self.supabase_url: str = os.environ.get("SUPABASE_URL")
        self.supabase_key: str = os.environ.get("SUPABASE_KEY")

        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Faltan variables de entorno SUPABASE_URL o SUPABASE_KEY")

        self.client: Client = create_client(self.supabase_url, self.supabase_key)


def get_filtered_songs(
    score_field: str, order_field: str, select_fields: List[str], min_score: float = 90
) -> List[dict]:
    """
    # Obtiene canciones filtradas de Supabase según los criterios especificados
    """
    try:
        supabase_manager = SupabaseManager()

        response = (
            supabase_manager.client.table("songs")
            .select(",".join(select_fields))
            .order(order_field, desc=True)
            .gte(score_field, min_score)
            .execute()
        )

        return response.data
    except Exception as e:
        raise Exception(f"Error al obtener datos de Supabase: {str(e)}")


def get_songs_with_value(
    selected_field: str, selected_score: str, response_fields: List[str]
) -> List[dict]:
    """
    # Obtiene canciones filtradas de Supabase según los criterios especificados
    """
    try:
        supabase_manager = SupabaseManager()

        if response_fields is None:
            response_fields = list(SongResponse.model_fields.keys())

        response = (
            supabase_manager.client.table("songs")
            .select(",".join(response_fields))
            .order("average_score", desc=True)
            .order(selected_field, desc=True)
            .eq(selected_field, selected_score)
            .execute()
        )

        return response.data
    except Exception as e:
        raise Exception(f"Error al obtener datos de Supabase: {str(e)}")


def get_songs_with_greater_or_equal(
    selected_field: str, response_fields: List[str], min_score: float = 90
) -> List[dict]:
    """
    # Obtiene canciones filtradas de Supabase según los criterios especificados
    """
    try:
        supabase_manager = SupabaseManager()

        if response_fields is None:
            response_fields = list(SongResponse.model_fields.keys())

        response = (
            supabase_manager.client.table("songs")
            .select(",".join(response_fields))
            .order(selected_field, desc=True)
            .gte(selected_field, min_score)
            .execute()
        )

        return response.data
    except Exception as e:
        raise Exception(f"Error al obtener datos de Supabase: {str(e)}")


def get_songs_with_zero_scores(
    empty_fields: List[str], order_field: str, response_fields: List[str] = None
) -> List[dict]:
    try:
        supabase_manager = SupabaseManager()

        # Si no se especifican campos de respuesta, usar los definidos en SongResponse
        if response_fields is None:
            response_fields = list(SongResponse.model_fields.keys())

        # Iniciar la consulta base
        query = supabase_manager.client.table("songs").select(",".join(response_fields))

        # Aplicar los filtros is_("null") para cada campo en empty_fields
        for field in empty_fields:
            query = query.is_(field, "null")

        # Aplicar el ordenamiento y ejecutar la consulta
        response = query.order(order_field, desc=True).execute()

        print(f"get_songs_with_zero_scores {response=}")
        return response.data

    except Exception as e:
        raise Exception(f"Error fetching data from Supabase: {str(e)}")