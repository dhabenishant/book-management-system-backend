from fastapi import APIRouter, HTTPException, status, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.utils.database import get_db
from app.utils.security import hash_password, verify_password, create_access_token
from app.schemas.user import RegisterRequest, LoginRequest, TokenResponse, UserOut
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    users_collection = db.get_collection("users")

    existing_user = await users_collection.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = hash_password(request.password)

    user_doc = {
        "name": request.name,
        "email": request.email,
        "hashed_password": hashed_password,
        "role": request.role,
        "created_at": __import__("datetime").datetime.utcnow(),
    }

    await users_collection.insert_one(user_doc)

    return {"message": "Registration successful. Please login.", "email": request.email}


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    users_collection = db.get_collection("users")

    user = await users_collection.find_one({"email": request.email})
    if not user or not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    user_id = str(user["_id"])
    access_token = create_access_token(data={"sub": user_id, "email": request.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile", response_model=UserOut)
async def get_profile(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    users_collection = db.get_collection("users")
    user_id = current_user["user_id"]

    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
    }
