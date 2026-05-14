from app import app
from models.user import User

with app.app_context():
    User.create("admin", "1234", "admin")
    print("Admin created")