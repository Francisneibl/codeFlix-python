from abc import ABC
from uuid import UUID

from src.core.genre.domain.Genre import Genre


class GenreRepository(ABC):
    def save(self, genre: Genre) -> None:
        raise NotImplementedError

    def get_by_id(self, genre_id: UUID) -> Genre | None:
        raise NotImplementedError

    def delete(self, genre_id: UUID) -> None:
        raise NotImplementedError

    def list(self) -> list[Genre]:
        raise NotImplementedError

    def update(self, genre: Genre) -> None:
        raise NotImplementedError
