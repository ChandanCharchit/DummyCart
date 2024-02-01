from fastapi import APIRouter, Query
from product_methods.v1_products import product_pool
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/dummy_cart/v1.0/products")


@router.get("/list_products/", tags=['PRODUCTS'], description="API to List all available products in the system.")
async def list_products(limit: int = Query(10, description="Number of products to fetch", gt=0),
                        offset: int = Query(0, description="Offset for pagination", ge=0),
                        min_price: int = Query(None, description="Minimum price filter"),
                        max_price: int = Query(None, description="Maximum price filter")):

    result = await product_pool.bring_products(limit, offset, min_price, max_price)
    return JSONResponse(content=result)

