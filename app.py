from flask import Flask
from flask_cors import CORS
from flask_restful import Api, reqparse
from routes.routes import initialize_routes

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    parser = reqparse.RequestParser()
    initialize_routes(api)
    app.run(host='0.0.0.0', port=6000, debug=True)