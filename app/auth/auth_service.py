from sqlalchemy import text
from models.crudpostgres import db_connect, db_close
from schemas.auth import UserCreate, UserLogin, UserResponse, Token
from schemas.response import success_response
from exceptions.custom_exceptions import ValidationError
from .jwt_handler import JWTHandler

class AuthService:
    """Service d'authentification simplifié"""

    @staticmethod
    def create_user(user_data: UserCreate):
        """Créer un nouvel utilisateur"""
        conn = db_connect()
        try:
            # Vérifier si l'email existe déjà
            existing_user = conn.execute(
                text("SELECT 1 FROM \"users\" WHERE email = :email"),
                {"email": user_data.email}
            ).fetchone()

            if existing_user:
                raise ValidationError("Un utilisateur avec cet email existe déjà")

            # Valider le rôle
            if user_data.role not in ["user", "admin"]:
                raise ValidationError("Le rôle doit être 'user' ou 'admin'")

            # Hacher le mot de passe
            password_hash = JWTHandler.hash_password(user_data.password)

            # Créer l'utilisateur
            result = conn.execute(
                text("""
                    INSERT INTO "users" (email, password_hash, role)
                    VALUES (:email, :password_hash, :role)
                    RETURNING id, email, role, is_active;
                """), {
                    "email": user_data.email,
                    "password_hash": password_hash,
                    "role": user_data.role
                }
            ).fetchone()
            conn.commit()

            # Créer une réponse utilisateur
            user_response = UserResponse(
                id=result.id,
                email=result.email,
                role=result.role,
                is_active=result.is_active
            )

            # Retourner une réponse de succès
            return success_response(
                data=user_response,
                message="Utilisateur créé avec succès"
            )
        finally:
            db_close(conn)

    @staticmethod
    def login(login_data: UserLogin):
        """Connecter un utilisateur"""
        conn = db_connect()
        try:
            # Chercher l'utilisateur par email
            user = conn.execute(
                text("SELECT id, email, password_hash, role, is_active FROM \"users\" WHERE email = :email"),
                {"email": login_data.email}
            ).fetchone()

            if not user:
                raise ValidationError("Email ou mot de passe incorrect")

            # Vérifier le mot de passe
            if not JWTHandler.verify_password(login_data.password, user.password_hash):
                raise ValidationError("Email ou mot de passe incorrect")

            # Vérifier que l'utilisateur est actif
            if not user.is_active:
                raise ValidationError("Compte désactivé")

            # Créer le token JWT
            access_token = JWTHandler.create_access_token(
                user_id=user.id,
                email=user.email,
                role=user.role
            )

            # Créer une réponse utilisateur
            user_response = UserResponse(
                id=user.id,
                email=user.email,
                role=user.role,
                is_active=user.is_active
            )

            # Retourner le token et les infos utilisateur
            token_response = Token(
                access_token=access_token,
                user=user_response
            )

            return success_response(
                data=token_response,
                message="Connexion réussie"
            )
        finally:
            db_close(conn)

    @staticmethod
    def get_current_user(token: str):
        """Récupérer l'utilisateur actuel depuis le token"""
        conn = db_connect()
        try:
            # Décoder le token
            payload = JWTHandler.decode_token(token)
            if not payload:
                raise ValidationError("Token invalide ou expiré")

            # Récupérer l'utilisateur
            user = conn.execute(
                text("SELECT id, email, role, is_active FROM \"users\" WHERE id = :user_id"),
                {"user_id": payload["user_id"]}
            ).fetchone()

            if not user:
                raise ValidationError("Utilisateur non trouvé")

            if not user.is_active:
                raise ValidationError("Compte désactivé")

            # Créer une réponse utilisateur
            user_response = UserResponse(
                id=user.id,
                email=user.email,
                role=user.role,
                is_active=user.is_active
            )

            return user_response
        finally:
            db_close(conn)

    @staticmethod
    def get_all_users():
        """Récupérer tous les utilisateurs (admin seulement)"""
        conn = db_connect()
        try:
            users = conn.execute(text("SELECT id, email, role, is_active FROM \"users\"")).fetchall()

            user_responses = [
                UserResponse(
                    id=user.id,
                    email=user.email,
                    role=user.role,
                    is_active=user.is_active
                ) for user in users
            ]

            return success_response(
                data=user_responses,
                message=f"{len(users)} utilisateurs trouvés"
            )
        finally:
            db_close(conn)
