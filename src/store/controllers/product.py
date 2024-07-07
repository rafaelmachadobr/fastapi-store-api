from typing import Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from pydantic import UUID4

from src.store.core.exceptions import NotFoundException
from src.store.schemas.product import (
    ProductIn,
    ProductOut,
    ProductUpdate,
    ProductUpdateOut,
)
from src.store.usecases.product import ProductUsecase

router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=ProductOut)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.create(body=body)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message
        ) from exc


@router.get(path="/{id}", status_code=status.HTTP_200_OK, response_model=ProductOut)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.get(path="/", status_code=status.HTTP_200_OK, response_model=list[ProductOut])
async def query(
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    usecase: ProductUsecase = Depends(),
) -> list[ProductOut]:
    return await usecase.query(min_price=min_price, max_price=max_price)


@router.patch(
    path="/{id}", status_code=status.HTTP_200_OK, response_model=ProductUpdateOut
)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
    try:
        return await usecase.update(id=id, body=body)
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    try:
        deleted = await usecase.delete(id=id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not found with id: {id}",
            )
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc
