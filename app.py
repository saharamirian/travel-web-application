from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


class Package:
    def __init__(self, destination, hotel, flights, activities, departure, price):
        self.destination = destination
        self.hotel = hotel
        self.flights = flights
        self.activities = activities
        self.departure = departure
        self.price = price


class PackageManage:
    def __init__(self):
        self.packages = {
            'iceland': Package('Iceland', 'Lagoon', 'Air Canada', 'Excursions', '6am 07/05/23', 2100),
            'greece': Package('Greece', 'Westin', 'Air Canada', 'Food Tour', '6am 07/05/23', 2000),
            'banff': Package('Banff', 'Fairmont', 'Air Canada', 'Guided Tour', '6am 07/05/23', 1900),
        }

    def get_packages(self, destination):
        return self.packages.get(destination)

    def represent_packages(self, destination):
        package = self.get_packages(destination)
        if package:
            report = {
                'Destination': package.destination,
                'Hotel': package.hotel,
                'Flights': package.flights,
                'Activities': package.activities,
                'Departure Time': package.departure,
                'Price': package.price
            }
            return report
        return None

    def search_destination(self, query):
        query = query.lower()
        if query in self.packages:
            return f'/{query}.html'
        return None

    def modify_package(self, destination, hotel, flights, activities, departure):
        if destination in self.packages:
            package = self.packages[destination]
            package.hotel = hotel
            package.flights = flights
            package.activities = activities
            package.departure = departure
            return True  # Return True if the modification was successful
        return False

    def create_table(self):
        connection = sqlite3.connect('packages.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination TEXT,
                hotel TEXT,
                flights TEXT,
                activities TEXT,
                departure TEXT,
                price INTEGER
            )
        ''')
        connection.commit()
        cursor.close()
        connection.close()

    def store_package(self, package):
        connection = sqlite3.connect('packages.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO packages (destination, hotel, flights, activities, departure, price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (package.destination, package.hotel, package.flights, package.activities, package.departure, package.price))
        connection.commit()
        cursor.close()
        connection.close()

    def show_database(self):
        connection = sqlite3.connect('packages.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM packages')
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows


class Travelcreation:
    def __init__(self, destination, hotel, flights, activities, departure, price):
        self.destination = destination
        self.hotel = hotel
        self.flights = flights
        self.activities = activities
        self.departure = departure
        self.price = price

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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search')
        package_manager = PackageManage()
        destination_url = package_manager.search_destination(search_query)
        if destination_url:
            return redirect(destination_url)
        else:
            return render_template('index.html', search_error=True)
    return render_template('index.html', search_error=False)


@app.route('/creation', methods=['GET', 'POST'])
def creation():
    package_manager = PackageManage()

    if request.method == 'POST':
        modification_mode = request.form.get('modification_mode')
        if modification_mode:
            destination = request.form.get('destination')
            hotel = request.form.get('hotel')
            flights = request.form.get('flights')
            activities = request.form.get('activities')
            departure = request.form.get('departure')
            package_manager.modify_package(destination, hotel, flights, activities, departure)
            return redirect(url_for('creation'))

    destination = request.form.get('destination')
    hotel = request.form.get('hotel')
    flights = request.form.get('flights')
    activities = request.form.get('activities')
    departure = request.form.get('departure')

    creation = Travelcreation(destination, hotel, flights, activities, departure, 0)
    total_price = creation.calculate_price()

    # Store the package in the database
    package_manager.store_package(creation)

    return render_template('creation.html', creation=creation, total_price=total_price)

@app.route('/iceland.html')
def iceland():
    package_manager = PackageManage()
    report = package_manager.represent_packages('iceland')
    return render_template('iceland.html', report=report)


@app.route('/greece.html')
def greece():
    package_manager = PackageManage()
    report = package_manager.represent_packages('greece')
    return render_template('greece.html', report=report)


@app.route('/banff.html')
def banff():
    package_manager = PackageManage()
    report = package_manager.represent_packages('banff')
    return render_template('banff.html', report=report)

@app.route('/<destination>.html')
def destination_page(destination):
    package_manager = PackageManage()
    report = package_manager.represent_packages(destination)
    if report:
        return render_template('destination.html', report=report)
    else:
        return redirect(url_for('index'))

@app.route('/database')
def view_database():
    package_manager = PackageManage()
    rows = package_manager.show_database()
    return render_template('database.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
