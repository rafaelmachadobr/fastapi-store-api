from pydantic import BaseModel, Field
from src.store.schemas.base import BaseSchemaMixin


class ProductBase(BaseModel):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: float = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")


class ProductIn(ProductBase, BaseSchemaMixin):
    ...


class ProductOut(ProductIn):
    ...
