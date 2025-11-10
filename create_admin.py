from passlib.context import CryptContext
from models import Admin
from database import SessionLocal

# Password hasher
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def create_default_admin():
    db = SessionLocal()

    # Check if admin already exists
    existing_admin = db.query(Admin).filter_by(username="admin").first()
    if existing_admin:
        print("⚠️ Admin already exists.")
        db.close()
        return

    admin = Admin(
        username="admin",
        password_hash=hash_password("admin123")
    )

    db.add(admin)
    db.commit()
    db.close()
    print("✅ Default admin created successfully!")

if __name__ == "__main__":
    create_default_admin()
