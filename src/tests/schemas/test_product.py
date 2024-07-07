from pydantic import ValidationError
import pytest
from src.store.schemas.product import ProductIn
from src.tests.factories import product_data


def test_schemas_validated():
    data = product_data()
    product = ProductIn.model_validate(data)

    assert product.name == "iPhone 15 Pro Max"


def test_schemas_return_error():
    data = {"name": "iPhone 15 Pro Max", "quantity": 10, "price": 8500.00}

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": {"name": "iPhone 15 Pro Max", "quantity": 10, "price": 8500.0},
        "url": "https://errors.pydantic.dev/2.8/v/missing",
    }
