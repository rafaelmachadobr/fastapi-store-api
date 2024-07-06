from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from src.store.core.exceptions import NotFoundException
from src.store.db.mongo import db_client
from src.store.schemas.product import (
    ProductIn,
    ProductOut,
    ProductUpdate,
    ProductUpdateOut,
)


class ProductUsecase:
    def __init__(self):
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product = ProductOut(**body.model_dump())
        await self.collection.insert_one(product.model_dump())

        return product

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        return ProductUpdateOut(**result)


product_usecase = ProductUsecase()
