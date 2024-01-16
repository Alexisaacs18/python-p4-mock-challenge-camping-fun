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

@app.route('/campers', methods=['GET', "POST"])
def get_campers():

    campers = [camper.to_dict() for camper in Camper.query.all()]
    
    if request.method == 'GET':
    
        response = make_response(
            campers,
            200
        )

    elif request.method == 'POST':
        try:
            form_data = request.get_json()
            new_camper = Camper(
                name = form_data["name"],
                age = form_data["age"]
            )

            db.session.add(new_camper)
            db.session.commit()

            response = make_response(
                new_camper,
                201
            )
        except ValueError:
            response = make_response(
                { "errors": ["validation errors"] },
                400
            )

    return response

@app.route('/campers/<int:id>', methods = ["GET", "PATCH"])
def campers_by_id(id):

    camper = Camper.query.filter(Camper.id == id).first()

    if request.method == "GET":

        try:

            response = make_response(
                camper.to_dict(),
                200
            )

        except: 
            response = make_response(
                {"Error": "Camper_ID does not exist"},
                404
            )

    elif request.method == "PATCH":

        try:
            
            form_data = request.get_json()

            for key in form_data:
                setattr(camper, key, form_data[key])

            db.session.commit()

            response = make_response(
                camper.to_dict(),
                201
            )

        except: 
            response = make_response(
                {"Error": "Camper_ID does not exist"},
                404
            )

    else:

        response = make_response(
            {"Error": "try a different method bro"},
            400
        )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
