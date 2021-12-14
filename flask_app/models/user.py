from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("Name must be at least 2 characters.", "register")
            is_valid = False
        if len(data['first_name']) < 2:
            flash("Name must be at least 2 characters.", "register")
            is_valid = False
        if (data['password'] != data['confirm_password']):
            flash("Passwords do not match", "register")
            is_valid = False
        if not email_regex.match (data['email']):
            flash("Email is not valid", "register")
            is_valid = False
        return is_valid

    @classmethod
    def insert_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email,password, confirm_password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(confirm_password)s)"
        return connectToMySQL("login_and_registration_schema").query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        user_db = connectToMySQL("login_and_registration_schema").query_db(query,data)
        if user_db: ## if it returns a boolean it can crash as a boolean is not less than 1 
            return cls(user_db[0])

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s"
        user_db = connectToMySQL("login_and_registration_schema").query_db(query,data)
        if user_db:
            return cls(user_db[0])