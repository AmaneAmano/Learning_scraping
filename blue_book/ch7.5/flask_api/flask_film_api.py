"""RESTful API for film table"""
from flask import Flask, abort
from flask_restful import Api, Resource, reqparse

# Import the class for Film table model from db.py
from db import Film

app = Flask(__name__)
# Make RESTful API instance
api = Api(app)


# Display single item
class FilmItem(Resource):
    """Specific Film"""
    def get(self, film_id):
        """Action when GET is executed"""
        try:
            # Fetch film data from film tabel searching film_id
            film = Film.get(Film.film_id == film_id)
        except Film.DoesNotExist:
            abort(404, description="Film not found")

        return film.to_dict()


# Display some items in a list
class FilmList(Resource):
    """Film list"""
    # Item count per page
    ITEMS_PER_PAGE = 5

    def __init__(self, *args, **kwargs):
        # Make a parser for GET parameters
        self.parser = reqparse.RequestParser()

        self.parser.add_argument('page', type=int, default=1)
        super().__init__(*args, **kwargs)

    def get(self):
        """Action when GET is executed"""
        args = self.parser.parse_args()
        # Fetch 5 items from film table in response to page parameter
        films = Film.select().order_by(Film.film_id).paginate(args['page'], self.ITEMS_PER_PAGE)

        return [film.to_dict() for film in films]


api.add_resource(FilmItem, '/film/<int:film_id>')
api.add_resource(FilmList, '/films')

if __name__ == "__main__":
    app.run(debug=True)