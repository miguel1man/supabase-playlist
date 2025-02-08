import uuid
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from models.song import SongResponse
from pathlib import Path
from supabase import create_client, Client
from typing import List, Optional, Union


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
        self,
        score_field: str,
        order_field: str,
        select_fields: List[str],
        min_score: float = 90,
    ) -> List[dict]:
        """
        # Obtiene canciones filtradas de Supabase según los criterios especificados
        """
        try:

            response = (
                self.client.table("songs")
                .select(",".join(select_fields))
                .order(order_field, desc=True)
                .gte(score_field, min_score)
                .execute()
            )

            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener datos de Supabase: {str(e)}")

    def get_songs_with_value(
        self, selected_field: str, selected_score: str, response_fields: List[str]
    ) -> List[dict]:
        """
        # Obtiene canciones filtradas de Supabase según los criterios especificados
        """
        try:
            if response_fields is None:
                response_fields = list(SongResponse.model_fields.keys())

            response = (
                self.client.table("songs")
                .select(",".join(response_fields))
                .order("previous_score", desc=True)
                .order(selected_field, desc=True)
                .eq(selected_field, selected_score)
                .execute()
            )

            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener datos de Supabase: {str(e)}")

    def get_songs_with_greater_or_equal(
        self, selected_field: str, response_fields: List[str], min_score: float = 90
    ) -> List[dict]:
        """
        # Obtiene canciones filtradas de Supabase según los criterios especificados
        """
        try:
            if response_fields is None:
                response_fields = list(SongResponse.model_fields.keys())

            response = (
                self.client.table("songs")
                .select(",".join(response_fields))
                .order(selected_field, desc=True)
                .gte(selected_field, min_score)
                .execute()
            )

            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener datos de Supabase: {str(e)}")

    def get_songs_by_score_range(
        self,
        score_field: str,
        response_fields: List[str],
        score_greater_or_equal: float = 90,
        score_less_than: float = 100,
    ) -> List[dict]:
        """
        # Obtiene canciones filtradas de Supabase según los criterios especificados
        """
        try:
            if response_fields is None:
                response_fields = list(SongResponse.model_fields.keys())

            response = (
                self.client.table("songs")
                .select(",".join(response_fields))
                .order(score_field, desc=True)
                .gte(score_field, score_greater_or_equal)
                .lt(score_field, score_less_than)
                .execute()
            )

            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener datos de Supabase: {str(e)}")

    def get_songs_with_zero_scores(
        self,
        empty_fields: List[str],
        order_field: str,
        response_fields: List[str] = None,
    ) -> List[dict]:
        try:
            # Si no se especifican campos de respuesta, usar los definidos en SongResponse
            if response_fields is None:
                response_fields = list(SongResponse.model_fields.keys())

            # Iniciar la consulta base
            query = self.client.table("songs").select(",".join(response_fields))

            # Aplicar los filtros is_("null") para cada campo en empty_fields
            for field in empty_fields:
                query = query.is_(field, "null")

            # Aplicar el ordenamiento y ejecutar la consulta
            response = query.order(order_field, desc=True).execute()

            print(
                f"Existen {len(response)} canciones con sin puntaje en los campos: {str(empty_fields)}"
            )
            return response.data

        except Exception as e:
            raise Exception(f"Error fetching data from Supabase: {str(e)}")

    def update_song(
        self,
        song_id: Union[str, int],
        selected_field: str,
        new_value: Union[str, int],
    ) -> List[dict]:
        """
        # Obtiene canciones filtradas de Supabase según los criterios especificados
        """
        try:

            response = (
                self.client.table("songs")
                .update({selected_field: new_value})
                .eq("id", song_id)
                .execute()
            )
            print(f"Updated song: {response}")

            return response.data
        except Exception as e:
            raise Exception(f"Error al actualizar datos: {str(e)}")

    def create_song(
        self,
        title: str,
        artist: str,
        youtube_url: Optional[str] = None,
        score_2025_01: Optional[int] = None,
    ) -> List[dict]:
        """
        Crea una canción en Supabase

        Args:
            title (str): Título de la canción.
            artist (str): Artista de la canción.
            youtube_url (Optional[str]): URL de YouTube de la canción (opcional).
            score_2025_01 (Optional[int]): Puntuación de la canción para enero de 2025 (opcional).
        """
        try:
            song_id = str(uuid.uuid4())
            now = datetime.now(timezone.utc)

            song_data = {
                "id": song_id,
                "title": title,
                "artist": artist,
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
            }

            if youtube_url is not None:
                song_data["youtube_url"] = youtube_url
            if score_2025_01 is not None:
                song_data["score_2025_01"] = score_2025_01

            print(f"{song_data=}")

            responseCreation = self.client.table("songs").insert(song_data).execute()
            print(f"Created song: {responseCreation}")

            return responseCreation.data[0]
        except Exception as e:
            raise Exception(f"Error al agregar una canción: {str(e)}")

    def get_song_list(self) -> List[dict]:
        """
        # Obtiene lista de canciones
        """
        try:

            responseList = self.client.table("songs").select("*").execute()
            print(f"Song list:\n{responseList}")

            return responseList.data
        except Exception as e:
            raise Exception(f"Error al obtener lista de canciones: {str(e)}")
