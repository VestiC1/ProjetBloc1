from fastapi import FastAPI
from api.routes import router as games_router
from api.auth_routes import router as auth_router


app = FastAPI(
    title="VestimLib - API Jeux Vidéo",
    description="""
    Bienvenue sur l'API Jeux Vidéo ! 🕹️

    Cette API vous permet de gérer et d'explorer des informations sur les jeux vidéo.
    Pour accéder aux fonctionnalités de l'API, vous devez d'abord créer un compte si vous n'en avez pas.
    Utilisez le endpoint `/auth/register` pour créer un compte.
    Une fois votre compte créé, vous pouvez vous connecter en utilisant le endpoint `/auth/login` pour obtenir un token d'accès.
    """,
    version="1.0.0",
        contact={
        "name": "Support",
        "email": "support@vestimlib.com",
    },
)

@app.get("/", tags=["Welcome"], summary="Page d'accueil de l'API")
def welcome():
    """
    Bienvenue sur la page d'accueil de l'API VestimLib.

    Ce point de terminaison fournit une introduction à l'API et des instructions de base
    pour commencer à utiliser les services de l'API. Il n'est pas nécessaire d'être
    authentifié pour accéder à cette page.

    Retourne un message de bienvenue et des instructions pour accéder aux fonctionnalités de l'API.
    """
    return {
        "message": "Bienvenue sur VestimLib l'API Jeux Vidéo ! 🕹️",
        "description": "Cette API vous permet de gérer et d'explorer des informations sur les jeux vidéo.",
        "instructions": "Pour accéder aux fonctionnalités de l'API, vous devez d'abord créer un compte si vous n'en avez pas. Vous trouverez toutes les informations sur `/docs` pour obtenir un token d'accès.",
    }

# Inclure les routes
app.include_router(auth_router)
app.include_router(games_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
