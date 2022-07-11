from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init DB
db = SQLAlchemy(app)
# Init Ma
ma = Marshmallow(app)

# Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=128), unique=True)
    description = db.Column(db.String(length=256))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "description", "price", "qty")


# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route("/api/product/", methods=["POST"])
def add_product():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Get All Product
@app.route("/api/product/", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)

    return jsonify(result)


# Get Single Product
@app.route("/api/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.filter_by(id=id).first()
    result = product_schema.dump(product)

    return jsonify(result)


# Update Product
@app.route("/api/product/<id>", methods=["PUT"])
def update_product(id):
    product = Product.query.filter_by(id=id).first()

    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product)


# Delete Single Product
@app.route("/api/product/<id>", methods=["DELETE"])
def delete_prodyct(id):
    product = Product.query.filter_by(id=id).first()

    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Run server
if __name__ == "__main__":
    app.run(debug=True)
