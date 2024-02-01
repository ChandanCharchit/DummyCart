from fastapi import APIRouter
from product_methods.v1_orders import order_book
from utils.models import CreateOrderRequest

router = APIRouter(prefix="/dummy_cart/v1.0/orders")


@router.post("/create_order", tags=['ORDERS'], description="API to Create a new order.")
async def create_order(order_request: CreateOrderRequest):
    return await order_book.create_new_order(order_request)

