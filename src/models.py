from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    favorites = db.relationship("Favorites",back_populates ="user" )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    
class Characters(db.Model):
    __tablename__ = 'characters'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)

    def serialize(self):
            return {
                "id": self.id,
                "eye_color": self.eye_color,
                "name": self.name,
                # do not serialize the password, its a security breach
            }
class Planets(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    gravity = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "terrain": self.terrain,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    vehicle_category = db.Column(db.String(250), nullable=False)
    make = db.Column(db.String(250), nullable=False)
   
    def serialize(self):
        return {
            "id": self.id,
            "make": self.make,
            "name": self.name,
            "vehicle_category": self.vehicle_category
           
        }
class Favorites(db.Model):
    __tablename__ = 'favorites'
# Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    fav_type = db.Column(db.Enum("character","planet"))

    user = db.relationship("User", back_populates="favorites")
    planet = db.relationship("Planets")
    character = db.relationship("Characters")
