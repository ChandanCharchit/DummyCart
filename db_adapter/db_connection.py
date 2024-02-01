from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import configparser

config = configparser.ConfigParser()

try:
    config.read('db_adapter/config.ini')
    db_url = config.get('Database', 'url')
    db_name = config.get('Database', 'db_name')

    client = AsyncIOMotorClient(db_url)
    db = client[db_name]
    products_catalog = db["dummy_products"]
    orders_catalog = db["orders"]
except configparser.NoSectionError as e:
    print(f"Error: {e}")
    print("Make sure the section 'Database' is present in config.ini")
    exit()


async def initialize_database():

    dummy_products = [
        {"name": "Toothpaste", "price": 200, "quantity": 25},
        {"name": "Dark Chocolate", "price": 400, "quantity": 15},
    ]

    await products_catalog.insert_many(dummy_products)


# asyncio.run(initialize_database())
