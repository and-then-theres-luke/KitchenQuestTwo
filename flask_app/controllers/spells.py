from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import spell


# Create


#Read
@app.route('/spells/search')
def spell_search_frontend():
    if 'user_id' not in session:
        return redirect("/login")
    return render_template("spell_search.html")

@app.route('/spells/show_one/<int:id>')
def show_spell_frontend(id):
    if 'user_id' not in session:
        return redirect("/login")
    one_spell = spell.Spell.get_spell_by_api_id(id)
    return render_template('one_spell.html', one_spell = one_spell)

@app.route('/spells/add_to_spellbook/', methods=['post'])
def add_to_spellbook_frontend():
    if 'user_id' not in session:
        return redirect('/login')
    data = {}
    for item in request.form:
        data[item] = request.form[item]
    if not spell.Userspell.add_to_spellbook(data):
        return redirect('/spells/show_one/' + request.form["api_spell_id"])
    return redirect('/dashboard')
