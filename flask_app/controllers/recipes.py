from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import recipe, spell
import pandas as pd
import requests

@app.route('/recipes/search')
def recipe_search_frontend():
    if 'user_id' not in session:
        return redirect("/login")
    return render_template("recipe_search.html")

@app.route('/recipes/show_one/<int:id>')
def show_one_recipe_frontend(id):
    if 'user_id' not in session:
        return redirect("/login")
    # Load Recipe
    one_recipe = recipe.Recipe.get_recipe_from_api(id)
    # Load User Spellbook
    spellbook = spell.Userspell.get_spellbook_by_user_id(session['user_id'])
    # Load required spells into DataFrame
    required_spells = pd.DataFrame(one_recipe.extended_ingredients)
    # Perform checks to see if spell is in spellbook
    for x in range(0,len(required_spells.index)):
        print(x["name"])
        for spell in spellbook:
            print(spell["id"])
            if required_spells[x['id']] == spell['id']:
                print("hello!")
            else:
                print("goodbye!")
    return redirect("/dashboard")
    return render_template("one_recipe.html", one_recipe = one_recipe, required_spells = required_spells, len = len(required_spells))
    return redirect('/dashboard')