#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/campers', methods=['GET'])
def get_campers():
    campers = [camper.to_dict() for camper in Camper.query.all()]

    # campers = []
    # camper = Camper.query.all()
    # for camper in campers:
    #     camper_dict = camper.to_dict()
    #     campers.append(camper_dict)
    
    response = make_response(
        campers,
        200
    )

    # campers = [camper.to_dict() for camper in Camper.query.all()]

    return response

@app.route('/campers/<int:id>')
def campers_by_id(id):
    try:
        camper = Camper.query.filter(Camper.id == id).first()

        response = make_response(
            camper.to_dict(),
            200
        )
    except: 
        response = make_response(
            {"Error": "Camper_ID does not exist"},
            404
        )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
