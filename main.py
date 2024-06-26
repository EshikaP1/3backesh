import threading

# import "packages" from flask
from flask import render_template,request  # import render_template from "public" flask libraries
from flask.cli import AppGroup


# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization

# setup APIs
from api.user import user_api # Blueprint import api definition
from api.player import player_api
from api.drink import drink_api
from api.fitness import fitness_api
#from api.pulse import pulse_api
from api.sleep import sleep_api
# from api.titanics import titanic_api
# database migrations
from model.users import initUsers
from model.players import initPlayers
from model.drinks import initDrinks
from model.fitnessy import initFitnessy
#from model.pulses import initPulses 
from model.sleeps import init_sleep
# from model.titanic import initTitanic
# from model.exercise import initExercise, predictWeight

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition


# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)
# initTitanic()

# initExercise()
# register URIs
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects) # register app pages
app.register_blueprint(drink_api)
app.register_blueprint(fitness_api)
# app.register_blueprint(titanic_api)
app.register_blueprint(sleep_api)
#app.register_blueprint(exercise_api)
@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

from flask import request, jsonify
# @app.route('/api/predict', methods=['POST'])
# def predict():
#     global exercise_regression
#     contestant = request.get_json()
#     response = predictWeight(contestant)
#     return jsonify(response)
# @app.route('/api/predictsurvival', methods=['POST'])

# Define the API endpoint for prediction

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4100', 'http://127.0.0.1:4100', 'https://eshikap1.github.io/2front/']:
        cors._origins = allowed_origin

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()
    initFitnessy()
    initDrinks()
    #initPulses()
    init_sleep()

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
        
# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="0.0.0.0", port="8008")
