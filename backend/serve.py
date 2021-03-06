import json
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_cors import CORS

# Local
import endpoints


app = Flask(__name__)
app.config['SERVER_NAME'] = 'crierapi.ashaltu.com'
CORS(app)
api = Api(app)

print(f"Creating endpoint resources...")
api.add_resource(endpoints.CreateToken, "/createtoken")
api.add_resource(endpoints.RemoveImages, "/removeimages")
api.add_resource(endpoints.AddImages, "/addimages")
api.add_resource(endpoints.SearchDatabase, "/search")
api.add_resource(endpoints.RetrieveImages, "/<token>/<imgname>")
print(f"Successfully installed endpoint resources")
print(f"Listening for requests...")

if __name__ == "__main__":
    app.run(host="localhost", port="5001", debug=True)
