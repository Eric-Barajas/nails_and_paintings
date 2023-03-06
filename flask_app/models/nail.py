from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from pprint import pprint

DATABASE = 'nails_and_paintings'

class Nail:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.sizes = data['sizes']
        self.shape = data['shape']
        self.color = data['color']
        self.theme = data['theme']
        self.price = data['price']
        self.user_id = data['user_id']
        self.description = data['description']
        if "first_name" in data:
            self.first_name = data['first_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def filter_nails(cls, data):
        query = "SELECT * FROM nails WHERE shape = %(shape)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        nails = []
        for u in results:
            nails.append( cls(u) )
        return nails
    
    @classmethod
    def get_all_nails(cls):
        query = 'SELECT * from nails;'
        results = connectToMySQL(DATABASE).query_db(query)
        nails = []
        for result in results:
            nails.append(Nail(result))
        return nails
