from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from db import db
from models import Department
import urllib.parse


app = Flask(__name__)

# Encode the username and password
username = urllib.parse.quote_plus('postgres')
password = urllib.parse.quote_plus('Imperial@2024')
database_name = 'University'

# Construct the database URI with encoded credentials
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@localhost:5432/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# Initialize db with the app
db.init_app(app)

# Reflect existing database tables (optional if you have manual models)
with app.app_context():
    db.reflect()  # Only needed if you use reflection

@app.route('/', methods=['GET', 'POST'])
def index():
    query_result = None
    if request.method == 'POST':
        selected_query = request.form.get('query_option')

        # Define allowed queries
        queries = {
            'all_departments': lambda: db.session.query(Department).all(),
            'specific_department': lambda: db.session.query(Department).filter_by(name='Sales').all(),
            # Add more queries as needed
        }

        # Execute the selected query
        query_func = queries.get(selected_query)
        if query_func:
            query_result = query_func()
        else:
            query_result = []

    return render_template('index.html', query_result=query_result)

if __name__ == '__main__':
    app.run(debug=True)
