# Project DummyCart

## Introduction

This FastAPI-based API serves as a foundation for a dummy shopping cart system. The code is organized into several modules, each handling specific aspects of the application.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- [Python](https://www.python.org/downloads/) (version 3.7 or higher)
- [pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone <https://github.com/ChandanCharchit/DummyCart.git>
   ```

2. Create a virtualenv and Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Database Configuration

1. Go to `db_adapter/setup_db.py` and keep the details as below 

    ```bash
   url = <your-database-url> or mongodb://localhost:27017/
   db_name = <your-database-name> or DummyKart
    ```
   
2. Go to `db_adapter/config.ini` file with the following content:

   ```ini
   [Database]
   url = <your-database-url> or mongodb://localhost:27017/
   db_name = <your-database-name> or DummyKart
   ```

   Replace `<your-database-url>` and `<your-database-name>` with your MongoDB connection URL and desired database name.

3. Save the `config.ini` file in the `db_adapter` directory.
4. Execute the following command to populate your database with dummy products.

```bash
python db_adapter/setup_db.py
```


## Running the Application

Execute the following command to start the FastAPI application:

```bash
uvicorn app:app --reload
```

This will start the API on `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs` or the alternative Swagger UI interface at `http://127.0.0.1:8000/redoc`.

## Project Structure
Certainly! Here's an example project structure documentation that you can use as a template. This assumes a basic project structure with some common components:

```plaintext
DummyCart
|-- db_adapter
|   |-- __init__.py
|   |-- config.ini
|   |-- db_connection.py
|   |-- setup_db.py
|-- logs
|   |-- app_logs.log
|-- product_methods
|   |-- __init__.py
|   |-- v1_orders.py.py
|   |-- v1_products.py
|-- routers
|   |-- __init__.py
|   |-- orders_apis.py
|   |-- products_apis.py
|-- utils
|   |-- __init__.py
|   |-- constants.py
|   |-- dummy_products.json
|   |-- logger.py.py
|   |-- models.py
|-- requirements.txt
|-- README.md
|-- app.py
```

- **app.py:** The main FastAPI application file that sets up the FastAPI instance and includes routing for products and orders.

- **routers/:** Contains router files for products (`products_apis.py`) and orders (`orders_apis.py`), defining API endpoints.

- **product_methods/:** Holds modules for handling product-related operations:
  - **`v1_products.py`**: Defines a `Product` class with a method to fetch and filter product data from a MongoDB collection.
  
  - **`v1_orders.py`**: Implements an `Order` class with methods to create a new order, validate product IDs, get product details, and update product quantities.

- **db_adapter/:** Manages the database connection and configuration in `db_connection.py` using the Motor library for MongoDB asynchronous operations.

- **utils/:** Contains utility modules:
  - **`logger.py`**: Sets up logging configuration for better visibility into the application's operations.
  
  - **`models.py`**: Defines data models used for request and response objects.

- **models.py:** Contains Pydantic models for handling data validation in API requests and responses:
  - **`Address`**: Represents the user's address with fields for city, country, and zip code.
  
  - **`OrderItem`**: Describes an item in an order with fields for product ID and bought quantity.
  
  - **`CreateOrderRequest`**: Represents the request body for creating a new order, containing a list of order items and user address. The `Config` class allows arbitrary types.

## API Endpoints

### Products API

- **List Products:**
  - **Endpoint:** `/dummy_cart/v1.0/products/list_products/`
  - **Method:** `GET`
  - **Description:** Retrieves a list of available products in the system.
  - **Query Parameters:**
    - `limit` (optional, default: 10): Number of products to fetch.
    - `offset` (optional, default: 0): Offset for pagination.
    - `min_price` (optional): Minimum price filter.
    - `max_price` (optional): Maximum price filter.

### Create Order API


**Request:**
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/dummy_cart/v1.0/products/list_products/?limit=10&offset=5&min_price=8000&max_price=12000' \
  -H 'accept: application/json'
```

**Response:**
```json
{
  "data": [
    {
      "_id": "65bc201a751c4a402b445faf",
      "name": "Fitness Tracker",
      "price": 8000,
      "quantity": 10
    },
    {
      "_id": "65bc201a751c4a402b445fb3",
      "name": "E-book Reader",
      "price": 9000,
      "quantity": 10
    }
  ],
  "page": {
    "limit": 10,
    "nextOffset": 15,
    "prevOffset": null,
    "total": 7
  }
}
```


### Create Order API

- **Create Order:**
  - **Endpoint:** `/dummy_cart/v1.0/orders/create_order`
  - **Method:** `POST`
  - **Description:** Creates a new order.
  - **Request Body:**
    - `order_request`: Request body containing order details.

Certainly! If you want to include this API call as a sample in your documentation, you can format it in a way that is easy for readers to understand. Here is an example of how you might present it in your documentation:

#### Sample Usage

**Request:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/dummy_cart/v1.0/orders/create_order' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "items": [
    {
      "product_id": "65bc201a751c4a402b445f9f",
      "bought_quantity": 5
    }
  ],
  "user_address": {
    "city": "Bengaluru",
    "country": "India",
    "zip_code": "560066"
  }
}'
```

**Request Body:**
```json
{
  "items": [
    {
      "product_id": "65bc201a751c4a402b445f9f",
      "bought_quantity": 5
    }
  ],
  "user_address": {
    "city": "Bengaluru",
    "country": "India",
    "zip_code": "560066"
  }
}
```

**Response:**
```json
{
  "Order placed successfully. Order id: ": "65bc23f3388ae13e99e569ed"
}
```
## Database Explanation

This FastAPI application utilizes MongoDB as its database backend. The MongoDB connection details are configured in the `db_adapter/config.ini` file.


### Database Collections

The application interacts with two collections:

1. **dummy_products:** Stores information about available products.

2. **orders:** Records details of customer orders.

### MongoDB Driver

The `db_adapter/db_connection.py` file manages the MongoDB connection using the Motor library. It establishes a connection to the specified database and provides access to the two collections mentioned above (`dummy_products` and `orders`).


## Exception Handling

The application employs FastAPI's exception handling mechanism to gracefully manage errors. Any errors during product listing or order creation result in appropriate HTTP status codes and error messages.

## Logging

Logging is configured using the `utils/logger.py` module for better visibility into the application's operations.

## Dependencies

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance), web framework for building APIs.
  
- [Motor](https://motor.readthedocs.io/en/stable/): An asynchronous MongoDB driver for Python, used for database operations.

- [Pydantic](https://pydantic-docs.helpmanual.io/): A data validation and settings management library.

## Conclusion

This FastAPI Dummy Cart application provides a simple yet extensible foundation for managing a basic shopping cart system. Developers can customize and expand the functionality to meet specific requirements. The project is structured for clarity and ease of maintenance, with Pydantic models ensuring data integrity in API requests and responses.





