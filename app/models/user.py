

class User:
    def __init__(self, id, email, password_hash, is_active=True, role="user"):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active
        self.role = role

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"

class UserInDB(User):
    def __init__(self, id, email, password_hash, is_active=True, role="user"):
        super().__init__(id, email, password_hash, is_active, role)
