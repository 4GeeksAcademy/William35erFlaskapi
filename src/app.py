"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Vehicles, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
def query_all(model):
    all_items = model.query.all()
    all_items_serialize = list(map(lambda item:item.serialize(),all_items))

    return jsonify(all_items_serialize), 200
def query_target_item(model,id):
    target_item = model.query.get(id)
    if target_item is None:
        return jsonify("no such item with provided id"), 400
    return jsonify(target_item.serialize()) 
@app.route('/user', methods=['GET'])
def handle_hello():

   
    return query_all(User)
@app.route('/people', methods=['GET'])
def get_all_people():
    return query_all(Characters)
@app.route('/people/<int:people_id>')
def get_target_person(people_id):
    return query_target_item(Characters,people_id)
@app.route('/planets', methods=['GET'])
def get_all_planets():
    return query_all(Planets)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
