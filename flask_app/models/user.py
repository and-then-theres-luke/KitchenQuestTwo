from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import spell
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = "kitchenquest" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.xp = data['xp']
        self.spellbook = []
        self.bosses = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    # Create Users Models
    @classmethod
    def create_user(cls, data):                 # Returns TRUE or FALSE
        if not cls.validate_new_user(data):
            return False
        query = """
            INSERT INTO users 
                (
                    first_name, 
                    last_name, 
                    email, 
                    password,
                    xp
                ) 
            VALUES 
                (
                    %(first_name)s, 
                    %(last_name)s, 
                    %(email)s, 
                    %(password)s,
                    0
                )
            ;
            """
        new_data = {
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'email' : data['email'],
            'password' : bcrypt.generate_password_hash(data['password'])
        }
        new_user = connectToMySQL(cls.db).query_db(query, new_data)
        new_user = User.get_user_by_id(new_user)
        session['user_id'] = new_user.id
        session['name'] = f"""{new_user.first_name} {new_user.last_name}"""
        return True


    # Read Users Models
    
    @classmethod
    def get_user_by_id(cls, id):                # Returns a user object or false
        data = {
            'id' : id
        }
        query = """
            SELECT *
            FROM users
            WHERE id = %(id)s
            ;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        one_user = cls(results[0])
        one_user.spellbook = spell.Userspell.get_spellbook_by_user_id(id)
        return one_user

    @classmethod
    def get_user_by_email(cls,email):           # Returns a user object or false
        data = {
            'email' : email
        }
        query = """
            SELECT * 
            FROM users 
            WHERE email = %(email)s
            ;
        """
        one_user = connectToMySQL(cls.db).query_db(query, data)
        if not one_user:
            return False
        return cls(one_user[0])
    
    # Update Users Models
    @classmethod
    def update_user(cls, data):              # Returns nothing
        query = """
            UPDATE users
            SET first_name = %(first_name)s, 
            last_name = %(last_name)s, 
            email = %(email)s,
            password = %(password)s
            WHERE id = %(id)s
            ;
        """
        connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def gain_xp(cls, xp_value):
        data = {
            'id' : session['user_id'],
            'xp_value' : xp_value
        }
        query = """
        UPDATE users
        SET xp = (xp + %(xp_value)s)
        WHERE id = %(id)s
        ;
        """
        connectToMySQL(cls.db).query_db(query, data)
        return
    
    # Delete Users Models
    @classmethod
    def delete_user(cls, data):     # Returns nothing
        if session['user_id'] != data['user_id']:
            flash("You don't have permissions to delete this account.", "delete_account")
            return
        query = """
            DELETE FROM users
            WHERE id = %(id)s;
        """
        connectToMySQL(cls.db).query_db(query, data)
        return
    
    # Validation Methods
    @staticmethod
    def validate_new_user(new_user):
        is_valid = True
        if User.get_user_by_email(new_user['email']):
            flash("Email is already registered to another user.", "register")
            is_valid = False
        if len(new_user['first_name']) < 3:
            flash("First name must be three (3) characters or more.", "register")
            is_valid = False
        if len(new_user['last_name']) < 3:
            flash("Last name must be three (3) characters or more.", "register")
            is_valid = False
        if len(new_user['password']) < 8:
            flash("Password must be 8 characters or more.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(new_user['email']): 
            flash("Invalid email address! Use less weird characters. Weirdo. So weird!", "register")
            is_valid = False
        if new_user['password'] != new_user['confirm_password']:
            flash("The passwords don't match! Try again.", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def login(data):
        one_user = None
        if not data['email']:
            flash("Please input a valid email.", 'login')
            return False
        if not data['password']:
            flash("Please input a valid password.", 'login')
            return False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'login')
            return False
        one_user = User.get_user_by_email(data['email']) # Changed my login validation a little so it returns either a class object or False
        if one_user:
            if not bcrypt.check_password_hash(one_user.password, data['password']):
                flash("Invalid email/password", "login")
                return False
        elif not one_user:
            flash("Invalid email/password", "login")
            return False
        session['user_id'] = one_user.id
        session['name'] = f"""{one_user.first_name} {one_user.last_name}"""
        return one_user