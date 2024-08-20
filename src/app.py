"""
This module takes care of starting the API Server, Loading the DB, and Adding the endpoints.
"""
import os
from flask import Flask, json, request, jsonify, url_for 
from flask_migrate import Migrate 
from flask_swagger import swagger 
from flask_cors import CORS 
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Planets, Characters, Favorites, User
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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

##########      METODO GET      ##########

@app.route('/user', methods=['GET'])
def get_user():
    all_user = User.query.all()
    result = [element.serialize() for element in all_user]
    response_body = {
        "message": "OK USER!!!",
        "planets": result
    }
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    result = [element.serialize() for element in all_planets]
    response_body = {
        "message": "OK PLANETS!!!",
        "planets": result
    }
    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    all_characters = Characters.query.all()
    result = [element.serialize() for element in all_characters]
    response_body = {
        "message": "OK PEOPLE!!!",
        "people": result
    }
    return jsonify(response_body), 200

@app.route('/favorites', methods=['GET'])
def get_favorites():
    all_favorites = Favorites.query.all()
    result = [element.serialize() for element in all_favorites]
    response_body = {
        "message": "OK FAVORITES!!!",
        "favorites": result
    }
    return jsonify(response_body), 200

##########      PEOPLE + PLANETS + USER // GET ID    ##########

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person_by_id(people_id):
    callCharacter = Characters.query.get(people_id)
    result = callCharacter.seralize()
    response_body = {"mensaje": "Character found!",}
    return jsonify(result), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets_by_id(planets_id):
    callPlanet = Planets.query.get(planets_id)
    result = callPlanet.seralize()
    response_body = {"mensaje": "Planet found!",}
    return jsonify(result), 200
    
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    callUser = Planets.query.get(user_id)
    result = callUser.seralize()
    response_body = {"mensaje": "User found!",}
    return jsonify(result), 200


##########      METODO POST      ##########

@app.route('/planets', methods= ['POST'])
def createPlanet():
    data= request.data
    data = json.loads(data)
    planet = Planets(name = data["name"], id = data["id"], diameter = data["diameter"], description = data["description"])
    db.session.add(planet)
    db.session.commit()
    response_body ={"message": "CREATE"}
    return jsonify(planet.serialize())


@app.route('/people', methods= ['POST'])
def createCharacter():
    data = request.data
    data = json.loads(data)
    character = Characters(name = data["name"], height = data["height"], gender = data["gender"], description = data["description"])
    db.session.add(character)
    db.session.commit()
    response_body = {"message": "CREATE"}
    return jsonify(character.serialize())


@app.route('/user', methods= ['POST'])
def createUser():
    data = request.data
    data = json.loads(data)
    newUser = User(name = data["name"], email = data["email"], id = data["id"], password = data["password"], is_active = data["is_active"])
    db.session.add(newUser)
    db.session.commit()
    response_body = {"message": "CREATE"}
    return jsonify(newUser.serialize())

##########      METODO DELETE      ##########

@app.route('/planets/<int:planets_id>', methods= ['DELETE'])
def deletePlanet(planets_id):
    planet = Planets.query.get(planets_id)
    db.session.delete(planet)
    db.session.commit()
    response_body = {"message": "DELETE"}
    return jsonify(planet.serialize())


@app.route('/people/<int:people_id>', methods= ['DELETE'])
def deletePeople(people_id):
    character = Characters.query.get(people_id)
    db.session.delete(character)
    db.session.commit()
    response_body = {"message": "DELETE"}
    return jsonify(character.serialize())


@app.route('/user/<int:user_id>', methods= ['DELETE'])
def deleteUser(user_id):
    byeUser = User.query.get(user_id)
    db.session.delete(byeUser)
    db.session.commit()
    response_body = {"message": "DELETE"}
    return jsonify(byeUser.serialize())

##########      FAVORITES      ##########

@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def fav_planet(planet_id):
    body_request = request.get_json()
    user_id = body_request.get("user_id", None)
    planet_id = body_request.get("planet_id", None)
    favoritePlanet = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(favoritePlanet)
    db.session.commit()
    response_body = {"message": "ADD"}
    return jsonify(favoritePlanet.serialize())


@app.route('/favorite/characters/<int:character_id>', methods=['POST'])
def fav_character(character_id):
    body_request = request.get_json()
    user_id = body_request.get("user_id", None)
    character_id = body_request.get("character_id", None)
    favoriteCharacter = Favorites(user_id=user_id, character_id=character_id)
    db.session.add(favoriteCharacter)
    db.session.commit()
    response_body = {"message": "ADD"}
    return jsonify(favoriteCharacter.serialize())


##########      DELETE FAVORITES      ##########

@app.route('/favorite/characters/<int:character_id>', methods= ['DELETE'])
def deleteFavCharacter(character_id):
    deleteCharacter = Favorites.query.get(character_id)
    db.session.delete(deleteCharacter)
    db.session.commit()
    response_body = {"message": "DELETE"}
    return jsonify(deleteCharacter.serialize())

@app.route('/favorite/planets/<int:planet_id>', methods= ['DELETE'])
def deleteFavPlanet(planet_id):
    deletePlanet = Favorites.query.get(planet_id)
    db.session.delete(deletePlanet)
    db.session.commit()
    response_body = {"message": "DELETE"}
    return jsonify(deletePlanet.serialize())


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
