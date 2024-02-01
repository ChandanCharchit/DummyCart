from fastapi.exceptions import HTTPException
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from db_adapter.db_connection import orders_catalog, products_catalog
from fastapi.responses import JSONResponse
from typing import List
from utils.models import OrderItem
from bson import ObjectId


async def create_new_order(order_request):
    try:
        # Validating product IDs and get product details
        product_details = await validate_and_get_product_details(order_request.items)

        # Total amount for each item
        for item in order_request.items:
            product_id = ObjectId(item.product_id)
            product_detail = product_details[str(product_id)]
            item.total_amount = product_detail["price"] * item.bought_quantity

        # Total order amount
        total_order_amount = sum(item.total_amount for item in order_request.items)

        # New order document
        order_document = {
            "createdOn": datetime.utcnow(),
            "items": jsonable_encoder(order_request.items),
            "user_address": jsonable_encoder(order_request.user_address),
            "total_order_amount": total_order_amount
        }
        result = await orders_catalog.insert_one(order_document)

        await update_product_quantities(order_request.items)

        return JSONResponse(content={"Order placed successfully. Order id: ": str(result.inserted_id)}, status_code=201)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error during creating new order due to: {str(ex)}")


async def validate_and_get_product_details(items: List[OrderItem]):
    try:
        # Product IDs from order items
        product_ids = [ObjectId(item.product_id) for item in items]

        # Finding the product IDs in product catalog
        product_details = await products_catalog.find({"_id": {"$in": product_ids}}).to_list(None)

        # Creating a dictionary with product details for quick lookup
        product_details_dict = {str(product["_id"]): product for product in product_details}
        print(product_details_dict)
        # Validating if all product IDs are found
        for item in items:
            if str(item.product_id) not in product_details_dict:
                raise HTTPException(status_code=400, detail=f"Product with ID {item.product_id} not found")

        return product_details_dict
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error validating new order due to: {str(ex)}")


async def update_product_quantities(order_items: List[OrderItem]):
    try:
        # Updating product quantities for each order item
        for item in order_items:
            product_id = ObjectId(item.product_id)
            bought_quantity = item.bought_quantity

            # Updating the product quantity by subtracting the bought quantity
            await products_catalog.update_one(
                {"_id": product_id},
                {"$inc": {"quantity": -bought_quantity}}
            )
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error in updating product quantities due to: {str(ex)}")
