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
@app.route('/planets/<int:planet_id>')
def get_target_planet(planet_id):
    return query_target_item(Planets,planet_id)
@app.route('/users/favorites/<int:user_id>')
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    favorites = user.serialize().get("favorites")
    return jsonify(favorites)
@app.route('/favorite/planet/<int:planet_id>',methods=['POST'])
def add_favorite_planets(planet_id):
    user_id =int(request.get_json()["uid"])
    new_Fav=Favorites(user_id = user_id, planet_id = planet_id, fav_type="planet")
    db.session.add(new_Fav)
    db.session.commit()
    return jsonify("favorite planet added succesfully"), 201
@app.route('/favorite/people/<int:people_id>',methods=['POST'])
def add_favorite_people(people_id):
    user_id =int(request.get_json()["uid"])
    new_Fav=Favorites(user_id = user_id, character_id = people_id, fav_type="character")
    db.session.add(new_Fav)
    db.session.commit()
    return jsonify("favorite people added succesfully"), 201
@app.route('/favorite/planet/<int:planet_id>',methods=['DELETE'])
def remove_favorite_planets(planet_id):
    user_id =int(request.args.get("uid"))
    Fav=Favorites.query.filter_by(user_id = user_id, planet_id = planet_id, fav_type="planet").first()
    db.session.delete(Fav)
    db.session.commit()
    return jsonify("favorite planet deleted succesfully"), 200
@app.route('/favorite/people/<int:people_id>',methods=['DELETE'])
def remove_favorite_people(people_id):
    user_id =int(request.args.get("uid"))
    Fav=Favorites.query.filter_by(user_id = user_id, character_id = people_id, fav_type="character").first()
    db.session.delete(Fav)
    db.session.commit()
    return jsonify("favorite people deleted succesfully"), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
