from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(80), unique=False, nullable=False)
    diameter = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "diameter": self.diameter,
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(80), nullable=True)
    height = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Characters %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "gender": self.gender,
            "height": self.height
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"), nullable=True)

    def __repr__(self):
        return '<Favorites %r>' % self.id 

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }
