from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from flask_app.models import user

class Build:
    db = 'car_clubs'
    def __init__(self, data):
        self.id = data['id']
        self.make_and_model = data['make_and_model']
        self.year_of_car = data['year_of_car']
        self.specs = data['specs']
        self.image_path = data['image_path']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

#CREATE
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO builds (make_and_model, year_of_car, specs, image_path, user_id)
        VALUES (%(make_and_model)s, %(year_of_car)s, %(specs)s, %(image_path)s, %(user_id)s)
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)



#READ
    @classmethod
    def get_builds(cls):
        query = """
        SELECT * FROM builds
        LEFT JOIN users ON
        user_id = users.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        builds = []
        for row in results:
            build = cls(row)
            user_data = {
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at'],
                "id": row['users.id']
            }
            build.creator = user.User(user_data)
            builds.append(build)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', builds)
        return builds



#UPDATE
    @classmethod
    def update(cls, data):
        query = """
        UPDATE builds SET
        make_and_model=%(make_and_model)s, year_of_car=%(year_of_car)s, specs=%(specs)s, image_path=%(image_path)s
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)


#Validate New Build
    @staticmethod
    def validate_build(data):
        is_valid = True
        if len(data['make_and_model']) < 1 :
            is_valid = False
            flash("Must have a make and model")
        if len(data['year_of_car']) < 1 :
            is_valid = False
            flash("Must have a year")
        if len(data['specs']) < 1 :
            is_valid = False
            flash("Must have specs for car")
        return is_valid



#DELETE
    @classmethod
    def delete_build(cls, id):
        data = {
            'id': id
        }
        query = """
        DELETE FROM
        builds WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)



#VIEW Build classmethod
    @classmethod
    def get_one_build(cls, id):
        data = {
            'id': id
        }
        query = """
        SELECT * FROM builds
        LEFT JOIN users ON
        user_id = users.id
        WHERE builds.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^', results)
        build = cls(results[0])

        user_data = {
                "first_name": results[0]['first_name'],
                "last_name": results[0]['last_name'],
                "email": results[0]['email'],
                "password": results[0]['password'],
                "created_at": results[0]['users.created_at'],
                "updated_at": results[0]['users.updated_at'],
                "id": results[0]['users.id']
        }
        build.creator = user.User(user_data)
        print('^^^^^^^^^^^^^^^^^^', build)
        return build



#Images
    @classmethod
    def get_image_path(cls, data):
        query = """
        SELECT image_path FROM
        builds
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results