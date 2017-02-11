from flask import Flask
import flask_restful
from scraper import FreeFoodScraper
from location_service import PrincetonBuildingLatLng
from food_service import CuisineParser
from dateutil import parser

import datetime


locations = PrincetonBuildingLatLng()
cuisine = CuisineParser()
app = Flask(__name__)
api = flask_restful.Api(app)

class FreeFoodServer(flask_restful.Resource):
    def get(self, month_id=None):
        if month_id is None:
            now = datetime.datetime.now()
            month = str(now.month)
            month = month if len(month) == 2 else "0"+month
            year = str(now.year % 2000)
            month_id = year + month
        food = FreeFoodScraper(month_id)

        listings = food.get_all()
        print 'Found', len(listings), 'listings'
        for listing in listings:
            building_name = locations.parse_building_name(listing['title'] + listing['body'])
            lat, lng = locations.get_lat_lng(building_name)
            listing['building_name'] = building_name
            listing['lat'] = lat
            listing['lng'] = lng

            listing['food_tags'] = cuisine.parse_food_tags(listing['title'] + ' ' + listing['body'])



        return sorted(listings, key=lambda x: parser.parse(x['time']), reverse=True)

api.add_resource(FreeFoodServer, '/', '/<month_id>')

if __name__ == '__main__':
    app.run(debug=True)
