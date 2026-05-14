from models.db import db
import hashlib

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def create(cls, username, password, role):
        user = cls(
            username=username,
            password=cls.hash_password(password),
            role=role
        )
        db.session.add(user)
        db.session.commit()

    @classmethod
    def verify(cls, username, password):
        hashed = cls.hash_password(password)
        return cls.query.filter_by(username=username, password=hashed).first()