from typing import Optional
from db_adapter.db_connection import products_catalog
from fastapi.exceptions import HTTPException
from utils.logger import setup_logger


class Product:
    def __init__(self):
        self.logger = setup_logger()

    async def bring_products(self, limit: int, offset: int, min_price: Optional[int], max_price: Optional[int]):
        try:
            # Aggregation pipeline
            pipeline = [
                {"$match": {}},
                {"$facet": {"data": [{"$skip": offset}, {"$limit": limit}], "total": [{"$count": "count"}]}},
            ]

            # Stages added for price filter
            if min_price is not None or max_price is not None:
                price_filter = {}
                if min_price is not None:
                    price_filter["$gte"] = min_price
                if max_price is not None:
                    price_filter["$lte"] = max_price

                pipeline[0]["$match"]["price"] = price_filter

            self.logger.info(f"Pipeline for the above request: {pipeline}")
            result = await products_catalog.aggregate(pipeline).to_list(1)

            for product in result[0]["data"]:
                product['_id'] = str(product['_id'])
            # Prepare response format
            response = {
                "data": result[0]["data"],
                "page": {
                    "limit": limit,
                    "nextOffset": offset + limit if result[0]["total"] else None,
                    "prevOffset": offset - limit if offset >= limit else None,
                    "total": result[0]["total"][0]["count"] if result[0]["total"] else 0,
                },
            }

            return response
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Error during fetching product list due to: {str(ex)}")


product_pool = Product()
