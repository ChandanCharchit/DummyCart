from typing import Optional
from db_adapter.db_connection import products_catalog
from fastapi.exceptions import HTTPException


async def bring_products(limit: int, offset: int, min_price: Optional[int], max_price: Optional[int]):
    try:
        # MongoDB aggregation pipeline for filtering and pagination
        pipeline = [
            {"$match": {}},
            {"$facet": {"data": [{"$skip": offset}, {"$limit": limit}], "total": [{"$count": "count"}]}},
        ]

        # Apply price filters if provided
        if min_price is not None:
            pipeline[0]["$match"]["price"] = {"$gte": min_price}
        if max_price is not None:
            pipeline[0]["$match"]["price"] = {"$lte": max_price}

        result = await products_catalog.aggregate(pipeline).to_list(1)

        # Prepare response format
        response = {
            "data": result[0]["data"],
            "page": {
                "limit": limit,
                "nextOffset": offset + limit if result[0]["total"] else None,
                "prevOffset": offset - limit if offset >= limit else None,
                "total": result[0]["total"][0]["count"],
            },
        }

        return response
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error during fetching product list due to: {str(ex)}")
