from fastapi import FastAPI
from api.routes import router


app = FastAPI(
    title="API Jeux Vidéo",
    description="Une API simple pour gérer les données des jeux vidéo",
    version="2.0.0"
)

# Inclure les routes
app.include_router(router)

@app.get("/")
def welcome():
    """Page d'accueil de l'API"""
    return {"message": "Bienvenue sur l'API Jeux Vidéo ! 🎮"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
