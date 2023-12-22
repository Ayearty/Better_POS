from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Users:
    DB="oover_eats_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.login = data['login']
        self.password = data['password']
        self.admin = data['admin']

    @staticmethod
    def validate_user(user):
        is_valid = True
        if user["first_name"] == "" or user["last_name"] == "" or user["login"] == "":
            flash("All fields required.")
            is_valid = False
        elif len(user['first_name']) < 2:
            flash("First name must be at least 3 characters.")
            is_valid = False
        elif len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        elif len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        elif user["pass_confirm"] != user["password"]:
            flash("Password and confirm password must match.")
            is_valid = False
        # elif ():
        #     is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name,last_name,login,password,admin) 
        VALUES (%(first_name)s,%(last_name)s,%(login)s,%(password)s,%(admin)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @staticmethod
    def validate_login(user):
        is_valid = True
        if user["login"] == None or user["password"] == None:
            flash("All fields required.")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_login(cls, data):
        query = "SELECT * from users WHERE login = %(login)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        else:
            return False

    @classmethod
    def get_one(cls, data):
        query  = """SELECT * FROM users WHERE id = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dishes;"
        results = connectToMySQL(cls.DB).query_db(query)
        dishes = []
        for dish in results:
            dishes.append( cls(dish) )
        return dish