from flask_app import app, api_key
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from datetime import date, timedelta
import requests
from flask import flash, session

class Spell:
    db = "kitchenquest"
    def __init__(self, data):
        self.api_spell_id = data['api_spell_id']        #This is used to match up with spells in the api.
        self.name = data['name']                        #Spell Name
        self.image = data['image']
        self.possible_units = data['possibleUnits']

    #API Pulls (Read Spell From API)
    @classmethod
    def get_spell_by_api_id(cls, api_ingredient_id):
        res = requests.get("https://api.spoonacular.com/food/ingredients/" + str(api_ingredient_id) + "/information?apiKey=" + "e5435bd9712a45208d0da9ad28db16b2")
        one_spell = res.json()
        data = {
            'api_spell_id' : one_spell['id'],
            'name' : (one_spell['name'].capitalize()),
            'aisle' : one_spell['aisle'],
            'image' : str("https://spoonacular.com/cdn/ingredients_500x500/" + one_spell['image']),
            'possibleUnits' : one_spell['possibleUnits']
        }
        return cls(data)

    @staticmethod
    def convert_amounts(api_spell_id, serving_amount, serving_unit, target_unit):
        print(api_spell_id, serving_amount, serving_unit, target_unit)
        if target_unit == "":
            targetAmount = serving_amount
        else:
            query = """https://api.spoonacular.com/recipes/convert?ingredientName=""" + str(api_spell_id) + """&sourceAmount=""" + str(serving_amount) + """&sourceUnit=""" + str(serving_unit) + """&targetUnit=""" + str(target_unit) + """&apiKey=""" + str(API_KEY)
            print("Converting " + str(serving_amount) + " " + str(serving_unit) + "to " + str(target_unit))
            res = requests.get(query)
            results = res.json()
            print(results)
            targetAmount = results['targetAmount']
            print("Result is: " + str(serving_amount) + " " + str(serving_unit) + " is equal to " + str(targetAmount) + " " + str(target_unit))
        return targetAmount

class Userspell(Spell):
    db = "kitchenquest"
    def __init__(self, data):
        super().__init__(data)
        self.id = data['id']                            #Unique id for this spell
        self.user_id = data['user_id']                  #This is what we use to build a user's spellbook
        self.current_servings = data['current_servings']  #Number of units left in the spell
        self.serving_value = data['serving_value']
        self.serving_unit = data['serving_unit']          #Let's say there are 8 servings of milk in a container. In the spellbook that would be represented as Current charges = 8, where one charge equals {{charge_amount}} {{charge_unit}} or in this case, 1 cup.
        self.isFrozen = data['isFrozen']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    #Create Spell
    @classmethod
    def add_to_spellbook(cls, data):
        print(data)
        if data['isFrozen'] == 'on':
            data['isFrozen'] = 1
        else:  
            data['isFrozen'] = 0
        if not cls.validate_new_spell(data):
            return False
        data['max_servings'] = data['current_servings']
        query = """
        INSERT INTO spells 
                (
                    user_id, 
                    api_spell_id,
                    name,
                    current_servings,
                    max_servings,
                    serving_value,
                    serving_unit,
                    expiration_date,
                    isFrozen
                ) 
            VALUES 
                (
                    %(user_id)s, 
                    %(api_spell_id)s,
                    %(name)s,
                    %(current_servings)s,
                    %(max_servings)s,
                    %(serving_value)s,
                    %(serving_unit)s,
                    %(expiration_date)s,
                    %(isFrozen)s
                )
            ;
        """
        if not connectToMySQL(cls.db).query_db(query, data):
            return False
        return True
    
    #Read Spellbook
    @classmethod 
    def get_spellbook_by_user_id(cls, user_id):
        spellbook = []
        data = {
            'id' : user_id
        }
        query = """
        SELECT *
        FROM spells
        WHERE user_id = %(id)s
        ;
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        if results == False:
            return spellbook
        for item in results:
            spellbook.append(cls(item))
        return spellbook
    
    # Validation Methods
    @staticmethod
    def validate_new_spell(data):
        isValid = True
        today = str(date.today())
        if int(data['current_servings']) <= 0:
            flash("Your ingredient needs at least one charge before you can add it to your pantry deck. Try again.","new_spell")
            isValid = False
        if data['expiration_date'] < today:
            flash("Expiration date cannot be in the past.","new_spell")
            isValid = False
        return isValid