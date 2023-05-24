from flask import Flask, render_template, request

app = Flask(__name__)

class Travelcreation:
    def __init__(self, destination, hotel, flights, activities, departure):
        self.destination = destination
        self.hotel = hotel
        self.flights = flights
        self.activities = activities
        self.departure = departure

    def get_destination(self):
        return self.destination

    def get_hotel(self):
        return self.hotel

    def get_flights(self):
        return self.flights

    def get_activities(self):
        return self.activities

    def get_departure(self):
        return self.departure

    def calculate_price(self):
        prices = {
            'New York': 1000,
            'Paris': 1200,
            'London': 800,
            'Rome': 900,
            'Montreal': 800,
            'Tokyo': 1000,
            'Toronto': 1100,
            'Vancouver': 1200,

            'Hilton': 200,
            'Holiday': 100,
            'Marriott': 300,

            'Air Canada': 500,
            'West Jet': 400,
            'Poter': 300,
            'Air Transit': 200,

            'guided tour': 100,
            'food': 50,
            'excursions': 200,
        }

        destination_price = prices.get(self.destination, 0)
        hotel_price = prices.get(self.hotel, 0)
        flights_price = prices.get(self.flights, 0)
        activities_price = prices.get(self.activities, 0)
        total_price = destination_price + hotel_price + flights_price + activities_price

        return total_price

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/creation', methods=['GET', 'POST'])
def creation():

    destination = request.form.get('destination')
    hotel = request.form.get('hotel')
    flights = request.form.get('flights')
    activities = request.form.get('activities')
    departure = request.form.get('departure')

    creation = Travelcreation(destination, hotel, flights, activities, departure)
    total_price = creation.calculate_price()

    return render_template('creation.html', creation=creation, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)

