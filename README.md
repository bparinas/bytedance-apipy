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
Display all events:
ex. curl -X GET 'http://<ip>:8000/events'
```

```
Event registration (duplicate email registration is not allowed per event):
ex. curl -X POST 'http://<ip>:8000/events' \
       -H 'Content-Type: application/json' \
       -d '{ "email": "md5@example.com", "event_name": "Conferences", "event_location": "Kyoto", "starttime": "2020-09-11 09:00:00", "endtime": "2020-09-11 17:00:00" }'
```

```
Remove registration by email
```
