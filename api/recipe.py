from contextlib import nullcontext
from flask import Blueprint, jsonify
from flask_restful import Api, Resource
import json
import random
from flask import request

recipe_api = Blueprint('recipe_api', __name__, url_prefix='/api/recipe')
api = Api(recipe_api)

def beautify_json_data(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        beautified_data = []
        for item in data.get('items', []):
            beautified_item = {
                "id": item.get("id", 0),
                "recipe": item.get("recipe", ""),
                "ingredients": item.get("ingredients", ""),
                "time": item.get("time", ""),
                "type": item.get("genre", ""),
            }

            beautified_data.append(beautified_item)

        return beautified_data

    except FileNotFoundError:
        return {"error": "File not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in the file"}

class _Read(Resource):
    def get(self):
        json_list = beautify_json_data('model/recipe.json')
        return jsonify(json_list)

class _ReadRandom(Resource):
    def get(self):
        beautified_data = beautify_json_data('model/recipe.json')
        random_item = random.choice(beautified_data)
        return jsonify(random_item)

class _Search(Resource):
    def get(self):
        query = request.args.get('query')
        if not query:
            return {"error": "No query provided"}, 400

        beautified_data = beautify_json_data('model/recipe.json')
        results = [item for item in beautified_data if query.lower() in item['recipe'].lower()]

        return jsonify(results)

class _Count(Resource):
    def get(self):
        beautified_data = beautify_json_data('model/recipe.json')
        count = len(beautified_data)
        return {"count": count}

api.add_resource(_Read, '/')
api.add_resource(_ReadRandom, '/random')
api.add_resource(_Search, '/search')
api.add_resource(_Count, '/count')