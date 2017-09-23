#!/usr/bin/python3
import time
import datetime
import psycopg2
import json
import requests
from config import config

def pullLaundryData():
    conn = None
    halls = ['TOWERS', 'BRACKENRIDGE', 'HOLLAND', 'LOTHROP', 'MCCORMICK','SUTH_EAST', 'SUTH_WEST', 'FORBES_CRAIG']
    try:
        params = config()
        print('Connecting to the PostgreSQL database')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        for hall in halls:
            r = requests.get('http://0.0.0.0:5000/laundry/simple/'+hall)
            data = json.loads(r.text)
            time = datetime.datetime.now().isoformat(' ')
            print(time)
            sql = """INSERT INTO laundrysimple(washers, dryers, time, hall) VALUES(%s, %s, %s, %s);"""

            cur.execute(sql, (data['free_washers'], data['free_dryers'], time, hall))
            conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    starttime=time.time()
    while True:
        pullLaundryData()
        time.sleep(5 * 60.0-((time.time()-starttime) % (5 * 60.0)))

