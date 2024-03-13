#Importing modules

from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

#Creating an app and configuring an SQLAlchemy Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#Creating Classes for Product and CartItem
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) #product id
    name = db.Column(db.String(100), nullable=False) #product name
    description = db.Column(db.Text, nullable=True) #product description
    price = db.Column(db.Float, nullable=False) #product price
    image_url = db.Column(db.String(200), nullable=True) #product image url

    def as_dict(self): #function to represent product as python dictionary
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class CartItem(db.Model): 
    id = db.Column(db.Integer, primary_key=True) #cart id
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False) #id of product in cart
    quantity = db.Column(db.Integer, nullable=False) #quantity of particular product

    #product = db.relationship('Product', backref=db.backref('cart_items', lazy=True)) #linking relationships

    def as_dict(self): #function to represent cartitem as python dictionary
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
# CRUD operations for Product
def create_product(name, description, price, image_url):
    product = Product.query.filter_by(name=name).first() #checking for duplicates
    if not product:
        product = Product(name=name, description=description, price=price, image_url=image_url)
        db.session.add(product)
        db.session.commit()
        db.session.close()
    return product

def get_product_by_id(product_id):
    return Product.query.get(product_id)

def update_product(product_id, name=None, description=None, price=None, image_url=None):
    product = get_product_by_id(product_id)
    if product:
        if name:
            product.name = name
        if description:
            product.description = description
        if price:
            product.price = price
        if image_url:
            product.image_url = image_url
        db.session.commit()
        db.session.close()
    return product

def delete_product(product_id):
    product = get_product_by_id(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        db.session.close()



        


#App Routing
@app.before_request
def create_tables():
    db.create_all()
    #Creating entries in our Database
    create_product(name='Apple', description='Fruit', price=100, image_url='example.com/image/')
    #create_product(name='Banana', description='Fruit', price=50, image_url='example.com/image/')
    #create_product(name='Mango', description='Fruit', price=150, image_url='example.com/image/')
    #create_product(name='Blueberries', description='Fruit', price=200, image_url='example.com/image/')
@app.route('/')
def Init():
    return("test")

@app.route('/products', methods=['GET'])
def get_products(): #returns a list of products in database
    products = Product.query.all()
    return jsonify([product.as_dict() for product in products])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id): #returns specific product by id
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.as_dict())
    else:
        abort(404, "Product not found")

@app.route('/cart', methods=['GET'])
def get_cart(): #returns all items in a cart
    cart_items = CartItem.query.all()
    return jsonify([item.as_dict() for item in cart_items])

@app.route('/cart', methods=['POST'])
def add_to_cart(): #adds product to cart
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    product = Product.query.get(product_id) #error handling
    if not product:
        abort(404, "Product not found") #if product not in db then abort

    cart_item = CartItem(product_id=product_id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()
    db.session.close()
    
    return jsonify({"message": "Product added to cart"})

@app.route('/cart/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id): #removes from cart
    cart_item = CartItem.query.get(item_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        db.session.close()
        return jsonify({"message": "Item removed from cart"})
    else:
        abort(404, "Item not found in cart") #if item not in cart then return error

if __name__ == '__main__':
    app.run(debug=False)
