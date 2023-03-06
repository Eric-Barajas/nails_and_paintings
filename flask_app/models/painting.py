from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from pprint import pprint

DATABASE = 'nails_and_paintings'

class Painting:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.date = data['date']
        self.measurement = data['measurement']
        self.price = data['price']
        self.user_id = data['user_id']
        if "first_name" in data:
            self.first_name = data['first_name']
        self.category = data['category']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # all the attributes are gonna be the columns in the ERD plus some


    # ! CREATE
    @classmethod
    def save(cls, data:dict) -> int:
        query = "INSERT INTO paintings (title, description, date, measurement, price, user_id) VALUES (%(title)s, %(description)s, %(date)s, %(measurement)s, %(price)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def filter_paintings(cls, data):
        query = "SELECT * FROM paintings WHERE category = %(category)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        paintings = []
        for u in results:
            paintings.append( cls(u) )
        return paintings

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM paintings;"
        results = connectToMySQL(DATABASE).query_db(query)
        paintings = []
        for u in results:
            paintings.append( cls(u) )
        return paintings

    # ! NEW
    @classmethod
    def get_all_items_from_cart(cls):
        query = "SELECT * FROM cart;"
        results = connectToMySQL(DATABASE).query_db(query)
        return results

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all_with_user(cls) -> list:
        query = "SELECT * FROM paintings JOIN users ON users.id = paintings.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        paintings = []
        for u in results:
            paintings.append( cls(u) )
        return paintings
    
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT * FROM paintings JOIN users on users.id = paintings.user_id WHERE paintings.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    # ! UPDATE
    @classmethod
    def update(cls,data:dict) -> int:
        query = "UPDATE paintings SET title=%(title)s,description=%(description)s, date=%(date)s, measurement=%(measurement)s price=%(price)s, user_id=%(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    # ! DELETE
    @classmethod
    def destroy(cls,data:dict):
        query  = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def add_painting_to_cart(cls, data):
        query = "INSERT INTO paintings_has_cart (painting_id, cart_id) VALUES (%(painting_id)s, %(cart_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def validate_painting(painting):
        is_valid = True
        if len(painting['title']) < 2:
            flash('title must be at least 2 characters.')
            is_valid = False
        if len(painting['description']) < 10:
            flash('Description must be at least 10 characters.')
            is_valid = False
        if len(painting['price']) < 0:
            flash('Price must be greater than 0')
            is_valid = False
        if len(painting['date']) < 0:
            flash('Date must be greater than 0')
            is_valid = False
        return is_valid