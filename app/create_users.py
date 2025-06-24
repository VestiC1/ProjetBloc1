from sqlalchemy import text
from models.crudpostgres import db_connect, db_close
from auth.jwt_handler import JWTHandler

"""
Pour Windows :
import sys
import os
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
"""

def create_default_users():
    """Créer des utilisateurs par défaut pour les tests"""
    print("👥 Création des utilisateurs par défaut")
    print("=" * 40)

    # Utilisateurs par défaut
    default_users = [
        {
            "email": "admin@games.com",
            "password": "admin123",
            "role": "admin"
        },
        {
            "email": "user@games.com",
            "password": "user123",
            "role": "user"
        },
        {
            "email": "jack@games.com",
            "password": "jacky123",
            "role": "user"
        }
    ]

    conn = db_connect()
    try:
        for user_data in default_users:
            # Vérifier si l'utilisateur existe déjà
            existing = conn.execute(text("SELECT 1 FROM \"users\" WHERE email = :email"), {"email": user_data["email"]}).fetchone()
            if existing:
                print(f"ℹ️ {user_data['email']} existe déjà")
                continue

            # Créer l'utilisateur
            password_hash = JWTHandler.hash_password(user_data["password"])
            conn.execute(text("""
                INSERT INTO "users" (email, password_hash, role)
                VALUES (:email, :password_hash, :role)
            """), {
                "email": user_data["email"],
                "password_hash": password_hash,
                "role": user_data["role"]
            })
            print(f"✅ Créé: {user_data['email']} ({user_data['role']})")

        conn.commit()
        print("\n🎉 Utilisateurs créés avec succès !")
        print("\n📋 Comptes de test disponibles:")
        print("👑 Admin: admin@games.com / admin123")
        print("👤 User: user@games.com / user123")
        print("👤 User: jack@games.com / rose123")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
        return False
    finally:
        db_close(conn)

if __name__ == "__main__":
    create_default_users()
