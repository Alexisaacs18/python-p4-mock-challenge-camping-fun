from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    signups = db.relationship("Signup", back_populates = "activities")
    
    serialize_rules = ("-signups.activities", )
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    signups = db.relationship("Signup", back_populates = "campers")
    
    serialize_rules = ("-signups.campers", )
    
    @validates("name")
    def validation_name(self, key, val):
        return val
    
    @validates("age")
    def validation_age(self, key, val):
        if val < 8:
            raise ValueError
        elif val > 18:
            raise ValueError
        else:
            return val
    
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))

    activities = db.relationship("Activity", back_populates = "signups")
    campers = db.relationship("Camper", back_populates = "signups")
    
    serialize_rules = ("-campers.signups", "-activities.signups")
    
    validates("time")
    def validation_time(self, key, val):
        if 0 <= val >= 23:
            return val
        else:
            raise ValueError
    
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
