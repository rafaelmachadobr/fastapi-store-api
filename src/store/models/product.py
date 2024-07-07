from src.store.models.base import CreateBaseModel
from src.store.schemas.product import ProductIn


class ProductModel(ProductIn, CreateBaseModel):
    ...
