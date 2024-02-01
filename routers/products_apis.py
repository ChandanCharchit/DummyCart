from fastapi import APIRouter, Query
from product_methods.v1_products import bring_products

router = APIRouter(prefix="/dummy_cart/v1.0/products")


@router.get("/list_products/", response_model=dict, tags=['PRODUCTS'])
async def list_products(limit: int = Query(10, description="Number of products to fetch", gt=0),
                        offset: int = Query(0, description="Offset for pagination", ge=0),
                        min_price: int = Query(None, description="Minimum price filter"),
                        max_price: int = Query(None, description="Maximum price filter")
):
    return await bring_products(limit, offset, min_price, max_price)
