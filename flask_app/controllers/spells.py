from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import spell


# Create
@app.route('/spells/view/<int:id>')
def view_spell_frontend(id):
    if 'user_id' not in session:
        return redirect('/login')
    one_spell = spell.Spell.get_spell_by_id(id)
    return render_template('one_spell.html', one_spell = one_spell)

