# Flask-E-Commerce-API
This project is a simple Flask-based backend API for a basic e-commerce platform. It demonstrates the implementation of RESTful API endpoints and integration with a SQLite database.

## Table of Contents

- [Setup](#setup)
- [Models](#models)
- [API Endpoints](#api-endpoints)
- [Database Integration](#database-integration)
- [Run the Application](#run-the-application)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Setup

### Install Dependencies

Create a file named app.py and copy the provided code into it.

Ensure you have Python installed on your system. Then, install the required dependencies using the following command:

## Configure Database
The application uses SQLite as the database. No additional setup is required for SQLite. If you wish to use a different database, update the SQLALCHEMY_DATABASE_URI in app.py accordingly.

## Models
The project includes two models:

Product: Represents a product with fields such as id, name, description, price, and image_url.
CartItem: Represents an item in a cart with fields such as id, product_id, and quantity.
API Endpoints
The following RESTful API endpoints are available:

GET /products: Returns a list of all products.
GET /products/<id>: Returns details of a specific product.
POST /cart: Adds a product to the cart.
GET /cart: Retrieves the cart items.
DELETE /cart/<id>: Removes a specific item from the cart.
Database Integration
The application uses SQLAlchemy for database integration. Tables for the models are created using db.create_all().

## Run the Application
To run the application, execute the following command in the terminal:

## bash
Copy code
python app.py
The application will be accessible at http://127.0.0.1:5000/.

## Testing
You can test the API using tools like curl or Postman. See the Testing section in the code explanation for example requests.

## Contributing
Feel free to contribute to this project by opening issues or pull requests. Any suggestions or improvements are welcome.

## License
This project is licensed under the MIT License.
