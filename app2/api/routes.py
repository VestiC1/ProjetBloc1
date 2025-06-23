from models.crudpostgres import db_connect, db_close
from sqlalchemy import text
from fastapi import APIRouter, HTTPException, Query
from schemas.games import GameShort, GameWithGenres
from typing import List

# parametre a voir prefix="/api/v1", tags=["games"]
router = APIRouter()

@router.get("/games", response_model=List[GameShort])
def get_games(
    page: int = Query(1, description="Numéro de la page", ge=1),
    per_page: int = Query(10, description="Nombre d'éléments par page", le=100)
):
    """Récupérer les jeux avec pagination"""
    offset = (page - 1) * per_page
    conn = db_connect()
    try:
        result = conn.execute(text(f'SELECT id,name FROM "Game" LIMIT :limit OFFSET :offset;'), {
            "limit": per_page,
            "offset": offset
        })
        games = [dict(row._mapping) for row in result]
        return games
    finally:
        db_close(conn)

@router.get("/games/genre/{genre}", response_model=List[GameWithGenres])
def get_games_by_genre(
    genre: str,
    page: int = Query(1, description="Numéro de la page", ge=1),
    per_page: int = Query(10, description="Nombre d'éléments par page", le=100)
):
    """Récupérer les jeux par genre avec pagination"""
    offset = (page - 1) * per_page
    conn = db_connect()
    try:
        result = conn.execute(text("""
            SELECT g.name, array_agg(DISTINCT ge.name) as genres
            FROM "Game" g
            JOIN "Game_Genre" gg ON g.id = gg.id_game
            JOIN "Genre" ge ON gg.id_genre = ge.id
            GROUP BY g.id, g.name
            HAVING :genre = ANY(array_agg(ge.name))
            LIMIT :limit OFFSET :offset;
        """), {"genre": genre, "limit": per_page, "offset": offset})

        games = [dict(row._mapping) for row in result]
        if not games:
            raise HTTPException(status_code=404, detail="Aucun jeu trouvé pour ce genre")
        return games
    finally:
        db_close(conn)
