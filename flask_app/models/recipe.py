from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import spell, recipe
from flask import flash, session
from flask_app.api_key import API_KEY
import requests


class Recipe:
    db = "kitchenquest"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.image = data['image']
        self.servings = data['servings']
        self.extended_ingredients = data['extendedIngredients']

    # Read Recipe
    @classmethod
    def get_recipe_from_api(cls, api_recipe_id):
        res = requests.get(
                            'https://api.spoonacular.com/recipes/' +
                            str(api_recipe_id) +
                            '/information?includeNutrition=false&apiKey=' + 
                            API_KEY)
        one_recipe = res.json()
        data = {
            'id' : one_recipe['id'],
            'title' : one_recipe['title'],
            'image' : one_recipe['image'],
            'servings' : one_recipe['servings'],
            'extendedIngredients' : one_recipe['extendedIngredients'],
        }
        one_recipe = cls(data)
        return one_recipe
