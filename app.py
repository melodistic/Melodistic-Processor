from flask import Flask
from flask_cors import CORS
from flask_restful import Api, reqparse
from singleton.prediction_model import PredictionModel
from routes.routes import initialize_routes

def setup():
    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    parser = reqparse.RequestParser()
    model = PredictionModel()
    initialize_routes(api)
    app.run(host='0.0.0.0', port=6000, debug=True)

if __name__ == '__main__':
    setup()