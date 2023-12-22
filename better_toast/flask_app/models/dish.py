from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Dish:
    DB="oover_eats_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.instructions = data['instructions']
        self.description = data['description']
        self.ingredients = data['ingredients']
        self.creator_id = data['creator_id']
        self.orders = data['orders']
        self.user = None

    @classmethod
    def save(cls, data ):
        query = """INSERT INTO dishes (title, instructions, description, ingredients,creator_id) 
        VALUES (%(title)s,%(instructions)s,%(description)s,%(ingredients)s,%(creator_id)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @staticmethod
    def validate_dish(dish):
        is_valid = True
        if dish["title"] == None or dish["instructions"] == None or dish["ingredients"] == None or dish["description"] == None:
            flash("All fields required.")
            is_valid = False
        if len(dish['title']) < 3:
            flash("Title must be more than 3 characters long.")
            is_valid = False
        if len(dish['description']) < 3:
            flash("Description must be more than 3 characters long.")
            is_valid = False
        if len(dish['instructions']) < 3:
            flash("Instructions must be more than 3 characters long.")
            is_valid = False
        if len(dish['ingredients']) < 3:
            flash("Recipe must be more than 3 characters long.")
            is_valid = False
        return is_valid
    
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM dishes WHERE id = %(id)s"
        data = {"id":id}
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM dishes WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        print (results)
        dish = cls(results[0])
        user_data = {"id" : dish.creator_id}
        dish.user = user.Users.get_by_id(user_data)
        return dish
    
    @classmethod
    def get_by_title(cls, data):
        query = "SELECT * from dishes WHERE title = %(title)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) > 0:
            return False
        elif len(results) == 0:
            return True

    @classmethod
    def update_one(cls,data):
        query = """
        UPDATE oover_eats_schema.dishes SET 
        title = %(title)s,
        instructions = %(instructions)s,
        ingredients = %(ingredients)s,
        description = %(description)s
        WHERE id=%(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def add_order(cls,data):
        query="""
        UPDATE oover_eats_schema.dishes SET
        orders = orders+1
        WHERE id = %(id)s
        """
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dishes;"
        results = connectToMySQL(cls.DB).query_db(query)
        dishes = []
        for dish in results:
            dishes.append( cls(dish) )
        return dishes
    
    @classmethod
    def end_day(cls):
        query = """
        UPDATE oover_eats_schema.dishes SET
        orders = 0
        """
        return connectToMySQL(cls.DB).query_db(query)
