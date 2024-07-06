from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.store.db.mongo import db_client
from src.store.schemas.product import ProductIn, ProductOut


class ProductUsecase:
    def __init__(self):
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product = ProductOut(**body.model_dump())
        await self.collection.insert_one(product.model_dump())

        return product


product_usecase = ProductUsecase()
