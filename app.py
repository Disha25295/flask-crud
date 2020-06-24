from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://disha:123456@localhost:3306/disha?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__= 'product'
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(100))
    productDescription = db.Column(db.String(100))
    productBrand = db.Column(db.String(100))
    price = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, title, productDescription, productBrand, price):
        self.title = title
        self.productDescription = productDescription
        self.productBrand = productBrand
        self.price = price
    
    def __repr__(self):
        return '' % self.id

db.create_all()

class ProductSchema(ModelSchema):
    class Meta (ModelSchema.Meta):
        model = Product
        sqla_session = db.session
    id = fields.Number(dump_only = True)
    title = fields.String(required=True)
    productDescription = fields.String(required = True)
    productBrand = fields.String(required = True)
    price = fields.Number(required = True)


@app.route('/product', methods = ['GET'])
def index():
    get_product = Product.query.all()
    product_schema = ProductSchema(many= True)
    products = product_schema.dump(get_product)
    return make_response(jsonify({'product': products}))

@app.route('/product', methods = ['POST'])
def create_product():
    data = request.get_json()
    product_schema = ProductSchema()
    product = product_schema.load(data)
    result = product_schema.dump(product.create())
    return make_response(jsonify({"product": result}),200)

@app.route('/product/<id>', methods = ['PUT'])
def update_product_by_id(id):
    data = request.get_json()
    get_product = Product.query.get(id)
    if data.get('title'):
        get_product.title = data['title']
    if data.get('productDescription'):
        get_product.productDescription = data['productDescription']
    if data.get('productBrand'):
        get_product.productBrand = data['productBrand']
    if data.get('price'):
        get_product.price = data['price']
    db.session.add(get_product)
    db.session.commit()
    product_schema = ProductSchema(only=['id','title','productDescription','productBrand','price'])
    product = product_schema.dump(get_product)
    return make_response(jsonify({"product": product}))

@app.route('/product/<id>', methods =  ['Delete'])
def delete_product_by_id(id):
    get_product = Product.query.get(id)
    db.session.delete(get_product)
    db.session.commit()
    return make_response("", 204)

if __name__ == "__main__":
    app.run(debug = True)