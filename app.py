from flask import Flask, jsonify, request, render_template
import os

app = Flask(__name__)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True    #<-This formats the output nicely.
 
stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
             'name': 'My item',
             'price': 15.99
            }
            
        ]
    }
]

@app.route("/")
def home():
    return render_template("index.html")




@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()  #get_json converts the json into a python dictionary so we can access it as below.
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)
    
    
@app.route("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})


@app.route("/store/")
def get_stores():
    return jsonify({'stores': stores})  
   
   
@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
        return jsonify({'message': 'store not found'})
    
   
@app.route("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})
   
   
   
   
   
   
   
   
   
   
   
   
    
if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))

