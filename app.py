from fastapi import FastAPI
from routers import products_apis, orders_apis

app = FastAPI()

app.include_router(products_apis.router)
app.include_router(orders_apis.router)
