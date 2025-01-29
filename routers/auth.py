from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.real_estate import User
import bcrypt

auth_router = APIRouter()
security = HTTPBasic()

# Define a Pydantic model for JSON-based login
class LoginRequest(BaseModel):
    username: str   
    password: str


class SignupRequest(BaseModel):
    username: str   
    password: str
    email: str
    firstname: str  
    lastname: str
    phone: str


@auth_router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    stored_password = user.password_hash  # This can be plain text or hashed

    # ✅ Check if password is stored as plain text
    if stored_password == request.password:
        print("Plain text password detected. Consider migrating to hashed passwords.")
        return {"user":user}

    # ✅ If password is hashed, use bcrypt to verify
    if stored_password.startswith("$2b$"):
        if bcrypt.checkpw(request.password.encode("utf-8"), stored_password.encode("utf-8")):
            return {"user":user}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

    # ❌ If password is neither plain text nor bcrypt hash, it's invalid
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid password format",
    )

@auth_router.post("/signup")   
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    # Check if the username is already
    user = db.query(User).filter(User.username == request.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    
    # Hash the password
    password_hash = bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt())

    # Create the new user
    new_user = User(
        username=request.username,
        email = request.email,
        password_hash=password_hash.decode("utf-8"),
        first_name = request.firstname,
        last_name = request.lastname,
        phone = request.phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user": new_user}

