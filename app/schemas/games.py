from pydantic import BaseModel
from typing import List, Optional


# Modèle Pydantic pour valider les données
class GameShort(BaseModel):
    id: int
    name: str

class GameWithGenres(BaseModel):
    name: str
    genres: List[str]

class GameDetail(BaseModel):
    id: int
    name: str
    cover: Optional[str]
    rating: Optional[int]
    rating_count: Optional[int]
    rating_opencritic: Optional[int]
    genres: List[str]
    platforms: List[str]
    companies: List[str]