from fastapi import APIRouter, HTTPException, status, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from app.utils.database import get_db
from app.schemas.book import CreateBookRequest, UpdateBookRequest, BookOut
from app.models.book import BooksListResponse
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/books", tags=["books"])


@router.post("", response_model=BookOut)
async def create_book(
    request: CreateBookRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    books_collection = db.get_collection("books")

    book_doc = request.dict()
    book_doc["created_by"] = current_user["user_id"]
    book_doc["created_at"] = datetime.utcnow()

    result = await books_collection.insert_one(book_doc)

    book_doc["_id"] = str(result.inserted_id)
    book_doc["created_at"] = book_doc["created_at"].isoformat()
    return book_doc


@router.get("", response_model=BooksListResponse)
async def list_books(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    category: str = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1, description="1 for ascending, -1 for descending"),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    books_collection = db.get_collection("books")

    query = {}
    if search:
        query["title"] = {"$regex": search, "$options": "i"}
    if category:
        query["category"] = category

    total = await books_collection.count_documents(query)

    skip = (page - 1) * limit
    sort_field = "created_at" if sort_by not in ["price", "published_date"] else sort_by

    books = await books_collection.find(query).sort(sort_field, sort_order).skip(skip).limit(limit).to_list(limit)

    books_list = [
        {
            **book,
            "_id": str(book["_id"]),
            "created_at": book["created_at"].isoformat(),
        }
        for book in books
    ]

    pages = (total + limit - 1) // limit

    return {
        "data": books_list,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages,
    }


@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    books_collection = db.get_collection("books")

    try:
        book = await books_collection.find_one({"_id": ObjectId(book_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid book ID",
        )

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    book["_id"] = str(book["_id"])
    book["created_at"] = book["created_at"].isoformat()
    return book


@router.put("/{book_id}", response_model=BookOut)
async def update_book(
    book_id: str,
    request: UpdateBookRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    books_collection = db.get_collection("books")

    try:
        book = await books_collection.find_one({"_id": ObjectId(book_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid book ID",
        )

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    update_data = {k: v for k, v in request.dict().items() if v is not None}

    if update_data:
        await books_collection.update_one({"_id": ObjectId(book_id)}, {"$set": update_data})

    updated_book = await books_collection.find_one({"_id": ObjectId(book_id)})
    updated_book["_id"] = str(updated_book["_id"])
    updated_book["created_at"] = updated_book["created_at"].isoformat()
    return updated_book


@router.delete("/{book_id}")
async def delete_book(
    book_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    books_collection = db.get_collection("books")

    try:
        result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid book ID",
        )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return {"message": "Book deleted successfully"}
