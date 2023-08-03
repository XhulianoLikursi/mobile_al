from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Car:
    db_name = 'mobileal'
    def __init__( self , data ):
        self.id = data['id']
        self.make = data['make']
        self.model = data['model']
        self.price = data['price']
        self.year = data['year']
        self.kilometer = data['kilometer']
        self.fuel = data['fuel']
        self.trasmission = data['trasmission']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_car_by_id(cls, data):
        query = "SELECT * FROM cars LEFT JOIN users on cars.user_id = users.id WHERE cars.id = %(car_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_all(cls):
        query = "SELECT * from cars LEFT JOIN users on cars.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        cars = []
        if results:
            for car in results:
                cars.append(car)
            return cars
        return cars
    #CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO cars (make, model, price, year, kilometer, fuel, transmission, description, user_id, image, phone_number) VALUES ( %(make)s, %(model)s, %(price)s, %(year)s, %(kilometer)s, %(fuel)s, %(transmission)s, %(description)s, %(user_id)s, %(image)s, %(phone_number)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET make = %(make)s, model = %(model)s,price = %(price)s, year = %(year)s, kilometer = %(kilometer)s, fuel = %(fuel)s, transmission = %(transmission)s, description = %(description)s WHERE cars.id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cars WHERE cars.id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def deleteAllParkings(cls, data):
        query = "DELETE FROM parkings WHERE car_id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def buy(cls, data):
        query = "INSERT INTO parkings (car_id, user_id) VALUES ( %(car_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    @classmethod
    def get_parked_cars(cls):
        query = "SELECT car_id as id from parkings;"
        results = connectToMySQL(cls.db_name).query_db(query)
        soldCars = []
        if results:
            for row in results:
                soldCars.append(row['id'])
            return soldCars
        return soldCars

    @staticmethod
    def validate_car(car):
        is_valid = True
        if len(car['model']) <1:
            flash('model title should be more than 2 characters!', 'model')
            is_valid= False
        if len(car['make']) <2:
            flash('make should be more than 2 characters!', 'make')
            is_valid= False
        if len(car['description']) <2:
            flash('descriprion should be more than 2 characters!', 'description')
            is_valid= False
        if len(car['fuel']) <2:
            flash('fuel should be more than 2 characters!', 'fuel')
            is_valid= False
        if len(car['transmission']) <2:
            flash('transmission should be more than 2 characters!', 'transmission')
            is_valid= False
        if car['price'] == "":
            flash('price shudent bbe emty...', 'price')
            is_valid= False
        if car['price'] != "":
            if int(car['price']) <= 0:
                flash('price shudent bbe emty...', 'price')
                is_valid= False
        if car['kilometer'] == "":
            flash('kilometer shudent bbe emty...', 'kilometer')
            is_valid= False
        if car['year'] == "":
            flash('year shudent bbe emty...', 'year')
            is_valid= False
        return is_valid
        