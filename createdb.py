import sqlite3

connection = sqlite3.connect('events.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS events (email text PRIMARY KEY, event_name text, event_location text, starttime datetime, endtime datetime, unique (email, event_name))"
cursor.execute(create_table)

events = [('sephy@example.com','Birthday','Tokyo','2020-09-09 10:00:00','2020-09-09 12:00:00'),
          ('yuna@example.com','Reunion','Osaka','2020-09-10 15:00:00','2020-09-10 21:00:00'), 
          ('uriel@example.com','Conferences','Kyoto','2020-09-11 09:00:00','2020-09-11 17:00:00')
         ]
cursor.executemany('INSERT INTO events VALUES(?,?,?,?,?);', events)

connection.commit()
connection.close()