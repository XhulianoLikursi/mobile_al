from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name = 'mobileal'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if results:
            for user in results:
                users.append(user)
            return users
        return users
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_bought_cars(cls, data):
        query = "SELECT cars.make as make, cars.model as model, cars.price as price, cars.year as year, cars.kilometer as kilometer, cars.fuel as fuel, cars.transmission as transmission, cars.phone_number as phone_number, cars.description as description, cars.image as image from parkings LEFT JOIN cars on parkings.car_id = cars.id WHERE parkings.user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        boughtCars = []
        if results:
            for row in results:
                boughtCars.append(row)
            return boughtCars
        return boughtCars


    @staticmethod
    def validate_user(user):
        is_valid = True
        
        if len(user['first_name']) <2:
            flash('First name should be more than 2 characters!', 'firstNameRegister')
            is_valid= False
        if len(user['last_name']) <2:
            flash('Last name should be more than 2 characters!', 'lastNameRegister')
            is_valid= False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailRegister')
            is_valid = False
        if len(user['password']) <8:
            flash('Password should be more then 8 characters!', 'passwordRegister')
            is_valid= False
        if user['password'] != user['confirmPassword']:
            flash('Passwords do not match!', 'confirmPasswordRegister')
            is_valid = False
        return is_valid
        