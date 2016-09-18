from flask import Flask
from flask.ext import restful
from scraper import FreeFoodScraper
from location_service import PrincetonBuildingLatLng
from dateutil import parser

food = FreeFoodScraper()
locations = PrincetonBuildingLatLng()
app = Flask(__name__)
api = restful.Api(app)

class FreeFoodServer(restful.Resource):
    def get(self):
        listings = food.get_all()
        print 'Found', len(listings), 'listings'
        for listing in listings:
            building_name = locations.parse_location(listing['title'] + listing['body'])
            lat, lng = locations.get_lat_lng(building_name)
            listing['building_name'] = building_name
            listing['lat'] = lat
            listing['lng'] = lng

        return sorted(listings, key=lambda x: parser.parse(x['time']), reverse=True)

api.add_resource(FreeFoodServer, '/')

if __name__ == '__main__':
    app.run(debug=True)
