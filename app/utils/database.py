import motor.motor_asyncio
from app.config import settings

client: motor.motor_asyncio.AsyncIOMotorClient = None
db: motor.motor_asyncio.AsyncIOMotorDatabase = None


async def connect_to_mongo():
    global client, db
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]
    print("Connected to MongoDB")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Closed MongoDB connection")


def get_db() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    return db
