from os import environ
from datetime import date, datetime
from flask import Flask
from flask_restful import reqparse, Resource, Api
from sqlalchemy import create_engine

# database engine settings
db_engine = create_engine('sqlite:///events.db')

# create and setup a parser for parsing incoming data in json format
parser = reqparse.RequestParser()
parser.add_argument('email', location='json')
parser.add_argument('event_name', location='json')
parser.add_argument('event_location', location='json')
parser.add_argument('starttime', location='json')
parser.add_argument('endtime', location='json')

# a class for serving API requests
class Events(Resource):

    # API endpoint http://<ip>:8000/events - display all events
    # ex. curl -X GET http://<replace-ip>:8000/events
    def get(self):
        # select all events data from the database
        db_conn = db_engine.connect()
        db_query = db_conn.execute("SELECT * FROM events")
        data = db_query.fetchall()

        items = []
        for row in data:
            items.append({'email': row[0], 'event_name': row[1], 'event_location': row[2], 'starttime': row[3], 'endtime': row[4]})
        
        return items

    # API endpoint - event registration
    # ex. curl -X POST 'http://<replace-ip>:8000/events' \
    # -H 'Content-Type: application/json' \
    # -d '{ "email": "md5@example.com", "event_name": "Conferences", "event_location": "Kyoto", "starttime": "2020-09-11 09:00:00", "endtime": "2020-09-11 17:00:00" }'
    def post(self):
        parsed_args = parser.parse_args()

        email = parsed_args['email']
        event_name = parsed_args['event_name']
        event_location = parsed_args['event_location']
        start_time = parsed_args['starttime']
        end_time = parsed_args['endtime']
        
        #validate start_time and end_time datetime format
        if start_time and end_time:
            try:
                datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                db_conn = db_engine.connect()
                db_query = db_conn.execute("INSERT INTO events VALUES(?,?,?,?,?)", email, event_name, event_location, start_time, end_time)
                result = { 'message': 'Congratulations! Your event registration has been successfully processed.' }
                code = 201 
            except ValueError:
                #display error message if datetime format is invalid
                result = { 'message': 'POST request has an invalid data, e.g. starttime/endtime must be in YYYY-MM-DD HH:MM:SS' }
                code = 400
        else:
            # the request doesn't contain a valid data
            result = { 'message': 'POST request must contain a valid datetime format. e.g. starttime/endtime YYYY-MM-DD HH:MM:SS' }
            code = 400
        return result, code


class EventUpdate(Resource):

    # API endpoint - update event registration ex. email data
    # ex. curl -X PUT 'http://<replace-ip>:8000/events/ilia@example.com' \
    # -H 'Content-Type: application/json' \
    # -d '{ "email": "md5@example.com" }'
    def put(self, email):
        parsed_args = parser.parse_args()

        new_email = parsed_args['email']
        
        # check if email exists in the database
        db_conn = db_engine.connect()
        db_query = db_conn.execute("SELECT * FROM events where email = '%s'" % (email))
        data = db_query.fetchone()

        #if found replace the old email with a new email data
        if data:
            db_query = db_conn.execute("UPDATE events SET email = '%s' WHERE email = '%s'" % (new_email, email))
            result = {}
            code = 204
            return result, code
        else:
            result = { 'message': 'Email not found.'}
            code = 500
            return result, code


class EventDelete(Resource):

    # API endpoint - delete event by email
    # ex. curl -X DELETE 'http://<replace-ip>:8000/events/ilia@example.com'

    def delete(self, email):

        # check if email exists in the database
        db_conn = db_engine.connect()
        db_query = db_conn.execute("SELECT * FROM events where email = '%s'" % (email))
        data = db_query.fetchone()

        #if found replace the old email with a new email data
        if data:
            db_query = db_conn.execute("DELETE FROM events WHERE email = '%s'" % (email))
            result = {}
            code = 204
            return result, code
        else:
            result = { 'message': 'Email not found.'}
            code = 500
            return result, code

# create a Flask application with API
app = Flask(__name__)
api = Api(app)

# create an API endpoint
api.add_resource(Events, '/events')
api.add_resource(EventUpdate, '/events/<string:email>')
api.add_resource(EventDelete, '/events/<string:email>')


# run the Flask application
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=8000)