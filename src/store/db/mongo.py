from motor.motor_asyncio import AsyncIOMotorClient
from src.store.core.config import settings


class MongoClient:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(
            settings.DATABASE_URL, uuidRepresentation="standard"
        )

    def get(self) -> AsyncIOMotorClient:
        return self.client


db_client = MongoClient()
