from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.database import connect_to_mongo, close_mongo_connection
from app.routes import auth, books

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


@app.get("/", tags=["root"])
async def root():
    return {"message": "Book Management System API", "version": "1.0.0"}


app.include_router(auth.router)
app.include_router(books.router)
