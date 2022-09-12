from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class User:
    db = 'car_clubs'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#CREATE
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def register_user(cls, data):
        if not cls.validate_user_reg_data(data):
            return False
        data = cls.parse_registration_data(data)
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query, data)
        print('>>>>>>>>>>>>>>>>>>>>>>>', user_id)
        session['user_id'] = user_id
        session['user_name'] = f"{data['first_name']} {data['last_name']}"
        return True






#READ
    @classmethod
    def getById(cls, data):
        query = """
        SELECT * FROM users 
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def getUserByEmail(cls, email):
        data = {'email': email}
        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            results = cls(results[0])
        return results


#UPDATE

#DELETE

#LOGIN VALIDATION
    @staticmethod
    def validate_user_reg_data(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2 :
            is_valid = False
            flash("first name needs to be at least 2 characters long")
        if len(data['last_name']) < 2 :
            is_valid = False
            flash("last name needs to be at least 2 characters long")
        if len(data['password']) < 8 :
            is_valid = False
            flash("password needs to be at least 8 characters long")
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email Format")
            is_valid = False
        if User.getUserByEmail(data['email'].lower()): 
            flash('That email is in use')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Your passwords don't match")
            is_valid = False
        return is_valid


    @staticmethod
    def parse_registration_data(data):
        parsed_data = {}
        parsed_data['email'] = data['email'].lower()
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data

    @staticmethod
    def login_user(data):
        this_user = User.getUserByEmail(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['user_name'] = f"{this_user.first_name} {this_user.last_name}"
                return True
        flash('Your login failed')
        return False