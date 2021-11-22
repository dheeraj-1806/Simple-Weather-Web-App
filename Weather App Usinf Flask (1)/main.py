import requests
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

class Coordinates(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    latitude = db.Column(db.Float, nullable = False)
    longitude = db.Column(db.Float, nullable = False)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        new_lat = request.form.get('lat')
        new_lon = request.form.get('lon')
        
        if new_lat and new_lon:
            new_coordinate_obj = Coordinates(latitude=float(new_lat), longitude=float(new_lon))

            db.session.add(new_coordinate_obj)
            db.session.commit()

    coordinates = Coordinates.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=07eec0d7b666c9a70378e1d5e5bb5f7f'

    weather_data = []

    for coordinate in coordinates:


        response = requests.get(url.format(coordinate.latitude,coordinate.longitude)).json()

        weather = {
            'coordinates' : {
                'latitude': coordinate.latitude,
                'longitude': coordinate.longitude,
            },
            'temperature' : response['main']['temp'],
            'description' : response['weather'][0]['description'],
        }

        weather_data.append(weather)

    return render_template('extra.html', weather_data=weather_data)



if __name__ == "__main__":
    app.run(debug=True)
