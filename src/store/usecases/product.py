from datetime import datetime
from typing import List, Optional
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from datetime import timezone
from src.store.core.exceptions import InsertionException, NotFoundException
from src.store.db.mongo import db_client
from src.store.models.product import ProductModel
from src.store.schemas.product import (
    ProductIn,
    ProductOut,
    ProductUpdate,
    ProductUpdateOut,
)


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())

        insert_result = await self.collection.insert_one(product_model.model_dump())

        if not insert_result.acknowledged:
            raise InsertionException(message="Error inserting product")

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(
        self, min_price: Optional[float] = None, max_price: Optional[float] = None
    ) -> List[ProductOut]:
        query_filter = {}

        if min_price:
            query_filter["price"] = {"$gte": min_price}

        if max_price:
            query_filter["price"] = {"$lte": max_price}

        if min_price and max_price:
            query_filter["price"] = {"$gte": min_price, "$lte": max_price}

        result_cursor = self.collection.find(query_filter)

        return [ProductOut(**item) async for item in result_cursor]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        update_data = body.model_dump(exclude_none=True)
        update_data["updated_at"] = datetime.now(timezone.utc)

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundException(f"Product with id {id} not found")

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})

        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return result.deleted_count > 0


product_usecase = ProductUsecase()
