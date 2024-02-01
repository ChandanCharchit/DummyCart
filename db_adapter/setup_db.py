import asyncio
import json
import configparser
from motor.motor_asyncio import AsyncIOMotorClient
from utils.constants import COLLECTION_PRODUCT


async def create_database_and_collection():
    try:
        db_url = "mongodb://localhost:27017/"
        db_name = "DummyKart"

        client = AsyncIOMotorClient(db_url)

        database = client[db_name]
        collection = database[COLLECTION_PRODUCT]

        json_file_path = '..\\utils\\dummy_products.json'
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        result = await collection.insert_many(data)
        print(f"Inserted {len(result.inserted_ids)} documents into the collection.")

        client.close()
    except configparser.NoSectionError as e:
        print(f"Error: {e}")
        print("Make sure the section 'Database' is present in config.ini")
        exit()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_database_and_collection())
