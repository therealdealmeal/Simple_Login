"""
    Sample Model File

    A Model should be in charge of communicating with the Database.
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import *
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()


    def create_user(self, info):

        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        # NAME_REGEX =  re.compile(r'^[a-zA-Z]+$')
        errors = False

        if not info['first_name']:
            errors.append('Name cannot be blank')
        elif len(info['first_name']) < 2:
            errors.append('Name must be at least 2 characters long')

        if not info['last_name']:
            errors.append('Name cannot be blank')
        elif len(info['last_name']) < 2:
            errors.append('Name must be at least 2 characters long')

        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')

        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')

        if info['password'] != info['pw_hash']:
            errors.append('Password and confirmation must match!')

        if errors:
            print errors
            return {"status": False, "errors": errors}
        else:
            password = info['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            create_query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at) VALUES (:first_name, :last_name, :email, :pw_hash, NOW())"
            create_data = {'first_name': info['first_name'], 'last_name': info['last_name'], 'email': info['email'], 'pw_hash': hashed_pw}
            query = "SELECT * FROM users"
            user_query = self.db.query_db(query)
            users = self.db.query_db(create_query, create_data)
            return { "status": True, "user": user_query[0]}


    def login_user(self, info):
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': info['email']}
        user = self.db.query_db(user_query, user_data)
        if user:
            if self.bcrypt.check_password_hash(user[0]['pw_hash'], info['password']):
                return { "status" : True, "user" : user[0] }
        return { "status" : False }
