from pydantic import BaseModel
from typing import List


# Modèle Pydantic pour valider les données
class GameShort(BaseModel):
    id: int
    name: str

class GameWithGenres(BaseModel):
    name: str
    genres: List[str]
