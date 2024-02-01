from fastapi.exceptions import HTTPException
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from db_adapter.db_connection import orders_catalog, products_catalog
from fastapi.responses import JSONResponse
from typing import List
from utils.models import OrderItem
from bson import ObjectId
from utils.logger import setup_logger


class Order:
    def __init__(self):
        self.logger = setup_logger()

    async def create_new_order(self, order_request):
        try:
            # Validating product IDs and get product details
            product_details = await self.validate_and_get_product_details(order_request.items)

            # Total amount
            total_order_amount = 0
            for item in order_request.items:
                product_id = ObjectId(item.product_id)
                product_detail = product_details[str(product_id)]
                total_order_amount += product_detail["price"] * item.bought_quantity

            # New order document
            order_document = {
                "createdOn": datetime.utcnow(),
                "items": jsonable_encoder(order_request.items),
                "user_address": jsonable_encoder(order_request.user_address),
                "total_order_amount": total_order_amount
            }
            result = await orders_catalog.insert_one(order_document)

            await self.update_product_quantities(order_request.items)
            self.logger.info(f"Order placed successfully having order id: : {str(result.inserted_id)}")

            return JSONResponse(content={"Order placed successfully. Order id: ": str(result.inserted_id)}, status_code=201)
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Error during creating new order due to: {str(ex)}")

    async def validate_and_get_product_details(self, items: List[OrderItem]):
        try:
            # Product IDs from order items
            product_ids = [ObjectId(item.product_id) for item in items]

            # Finding the product IDs in product catalog
            product_details = await products_catalog.find({"_id": {"$in": product_ids}}).to_list(None)

            # Creating a dictionary with product details for quick lookup
            product_details_dict = {str(product["_id"]): product for product in product_details}

            # Validating if all product IDs are found
            for item in items:
                if str(item.product_id) not in product_details_dict:
                    self.logger.info(f"Product id {item.product_id} not found in product list.")
                    raise HTTPException(status_code=400, detail=f"Product with ID {item.product_id} not found")

            return product_details_dict
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Error validating new order due to: {str(ex)}")

    async def update_product_quantities(self, order_items: List[OrderItem]):
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
                self.logger.info(f"Updated order quantity of product {product_id}.")
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Error in updating product quantities due to: {str(ex)}")


order_book = Order()
