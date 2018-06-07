from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
import os


app = Flask(__name__)
app.secret_key = "colm"
api = Api(app)

jwt = JWT(app, authenticate, identity) #JWT class creates a new endpoint /auth, when we call /auth we send it a username and password that is used in authenticate and identity.

items = []

class Item(Resource): #Our new Student class inherits from Resource, we don't have to use jsonify because the Resource class does it.
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    
    
    @jwt_required() #decorator, it means we have to authenticate before we can call the get method.
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        item = next(filter(lambda x: x['name'] == name ,items), None) #next method will return the first result from lambda function or None 
        return {'item': item}, 200 if item else 404 #Ternary if statement
        
    def post(self, name):
        if next(filter(lambda x: x['name'] == name ,items), None):
            return {'Message': 'An item with name {}, already exists'.format(name)}, 400
            
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201
        
        
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items)) #overwriting our list with the same list minus the one we are deleting.
        return {'message': 'Item deleted'}
        
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name ,items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item
            
        
        
class ItemList(Resource):
    def get(self):
        return {'items': items}
        
        
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=True)