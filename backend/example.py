import json
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_cors import CORS
from enom_server import EnOmTranslator

app = Flask(__name__)
app.config['SERVER_NAME'] = '40.122.200.108:5000'
CORS(app)
api = Api(app)

model_dir = "en-om-30k-v1-fast"
translator = EnOmTranslator(model_dir=model_dir)

class TranslateSentence(Resource):
    def get(self):
        return {"ErrorMessage": "Request should be POST."}

    def post(self):
        data = request.get_json(force=True)

        if 'english' in data:
            data = jsonify({"oromo": translator.translate(data['english']), 'success': True})
            return make_response(data, 200)

        elif 'oromo' in data:
            # Need to implement back translations (oromo -> english)
            data = jsonify({"english": translator.translate(data['oromo']), 'success': True})
            return make_response(data, 200)

        return {"ErrorMessage": "Invalid POST message."}, 201

class TranslateParagraph(Resource):
    def get(self):
        return {"ErrorMessage": "Request should be POST."}

    def post(self):
        data = request.get_json(force=True)
        if 'english' in data:
            data = jsonify({"oromo": translator.translate(data['english']), 'success': True})
            return make_response(data, 200)

        elif 'oromo' in data:
            # Need to implement back translations (oromo -> english)
            data = jsonify({"english": translator.translate(data['english']), 'success': True})
            return make_response(data, 200)

        return {"ErrorMessage": "Invalid POST message."}, 201

api.add_resource(TranslateSentence, "/sentence")
api.add_resource(TranslateParagraph, "/paragraph")

if __name__ == "__main__":
    app.run(host="localhost", port="5000", debug=True)
