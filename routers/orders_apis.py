from fastapi import APIRouter
from product_methods.v1_orders import create_new_order
from utils.models import CreateOrderRequest

router = APIRouter(prefix="/dummy_cart/v1.0/orders")


@router.post("/create_order", response_model=dict, tags=['ORDERS'])
async def create_order(order_request: CreateOrderRequest):
    return await create_new_order(order_request)

