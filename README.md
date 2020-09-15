### Howto setup the environment
```
git clone https://github.com/bparinas/bytedance-apipy.git
cd bytedance-apipy
virtualenv venv --python=python3.7
source venv/bin/activate

# Install package dependencies
pip install -r requirements.txt

# Create the events.db sqlite database
python createdb.py

# Start the program
python src/app.py
```

### API endpoint testing (manual w/curl)
```
# Display all events
ex. curl -X GET 'http://<ip>:8000/events'
```

```
# Successful event registration
ex. curl -X POST 'http://<ip>:8000/events' \
       -H 'Content-Type: application/json' \
       -d '{ "email": "md5@example.com", "event_name": "Conferences", "event_location": "Kyoto", "starttime": "2020-09-11 09:00:00", "endtime": "2020-09-11 17:00:00" }'

201 {"message": "Congratulations! Your event registration has been successfully processed."}
```
```
# Duplicate email registration is not allowed per event (e.i adding data that already exists)
ex. curl -X POST 'http://34.70.25.201:8000/events' \
     -H 'Content-Type: application/json' \
     -d '{ "email": "uriel@example.com", "event_name": "Conferences", "event_location": "Kyoto", "starttime": "2020-09-11 09:00:00", "endtime": "2020-09-11 17:00:00" }'
	 
Log snippets...
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: events.email, events.event_name
[SQL: INSERT INTO events VALUES(?,?,?,?,?)]
[parameters: ('uriel@example.com', 'Conferences', 'Kyoto', '2020-09-11 09:00:00', '2020-09-11 17:00:00')]
```
```
# Invalid datetime format
ex. curl -X POST 'http://34.70.25.201:8000/events' \
         -H 'Content-Type: application/json' \
	 -d '{ "email": "ilia@example.com", "event_name": "Conferences", "event_location": "Kyoto", "starttime": "2020-09-11 09:00:00", "endtime": "2020-09-11 17:00" }'
400 {"message": "POST request has an invalid data, e.g. starttime/endtime must be in YYYY-MM-DD HH:MM:SS"}

    curl -X POST 'http://34.70.25.201:8000/events' \
         -H 'Content-Type: application/json' \
	 -d '{ "email": "ilia@example.com", "event_name": "Conferences", "event_location": "Kyoto", "starttime": "2020-09-11 09:00", "endtime": "2020-09-11 17:00" }'
400 {"message": "POST request has an invalid data, e.g. starttime/endtime must be in YYYY-MM-DD HH:MM:SS"}
```

```
# Update event registration (i.e. email data)
Email sephy@example.com has an existing event registration record. New email will be used.
curl -X PUT http://34.70.25.201:8000/events/sephy@example.com -H 'Content-Type: application/json' -d '{ "email": "ilia@example.com" }'

Email nullx@example.com has no event registration record
curl -X PUT http://34.70.25.201:8000/events/nullx@example.com -H 'Content-Type: application/json' -d '{ "email": "ilia@example.com" }'
{"message": "Email not found."}
```

```
**Remove registration by email**
```
