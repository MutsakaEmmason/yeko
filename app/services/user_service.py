import bcrypt
from app.utils.db import SessionLocal
from app.models.models import User, Role


def get_all_users():
    with SessionLocal() as session:
        users = session.query(User).join(Role).all()
        return [{
            "ID": u.user_id,
            "Name": u.name,
            "Email": u.email,
            "Role": u.role.role_name if u.role else "None"
        } for u in users]


def authenticate_user(email: str, password: str):
    with SessionLocal() as session:
        user = session.query(User).filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            return {
                "id": user.user_id,
                "name": user.name,
                "email": user.email,
                "role": user.role.role_name if user.role else "None"
            }
        return None


def add_user(name, email, password, role_id):
    with SessionLocal() as session:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(name=name, email=email, password=hashed, role_id=role_id)
        session.add(user)
        session.commit()
