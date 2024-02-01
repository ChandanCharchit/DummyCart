from motor.motor_asyncio import AsyncIOMotorClient
import configparser
from utils.constants import DATABASE, COLLECTION_ORDER, COLLECTION_PRODUCT, CONFIG_FILE_PATH

config = configparser.ConfigParser()

try:
    config.read(CONFIG_FILE_PATH)

    db_url = config.get(DATABASE, 'url')
    db_name = config.get(DATABASE, 'db_name')

    client = AsyncIOMotorClient(db_url)
    db = client[db_name]
    products_catalog = db[COLLECTION_PRODUCT]
    orders_catalog = db[COLLECTION_ORDER]
except configparser.NoSectionError as e:
    print(f"Error: {e}")
    print("Make sure the section 'Database' is present in config.ini")
    exit()
