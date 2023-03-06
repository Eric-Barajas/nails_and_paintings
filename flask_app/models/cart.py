from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from pprint import pprint
from flask_app.models.painting import Painting

DATABASE = 'nails_and_paintings'


class Cart:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # @classmethod
    # def show_items_in_cart(cls):
    #     query ="SELECT * FROM cart;"
    #     result = connectToMySQL(DATABASE).query_db(query)
    #     return result

    @classmethod
    def show_items_in_cart(cls, data):
        query = "SELECT * FROM carts JOIN paintings_has_cart ON carts.id = paintings_has_cart.cart_id JOIN paintings ON paintings_has_cart.painting_id = paintings.id WHERE carts.id = %(id)s ;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        paintings = []
        for painting in results:
            temp_painting = {
                'id' : painting['paintings.id'],
                'title' : painting['title'],
                'description' : painting['description'],
                'date' : painting['date'],
                'measurement' : painting['measurement'],
                'price' : painting['price'],
                'user_id' : painting['paintings.user_id'],
                'category' : painting['category'],
                'created_at' : painting['paintings.created_at'],
                'updated_at': painting['paintings.updated_at']
            }
            paintings.append(Painting(temp_painting))
        return paintings



