import sqlite3
import psycopg2
import os
import json
import io
import csv
import maidenhead as mh
from flask import Flask
from flask import render_template, make_response

app = Flask(__name__)

@app.route('/')
def main():
  return render_template('main.html')

@app.route('/checkins')
def checkins():
    calls = list_table_content()
    return render_template('checkins.html', entries=calls)

def list_table_content():
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    cursor.execute("SELECT callsigns,name,locator,bands,modes,schedule,comment,DATE(last_checkin) FROM checkins;")
    calls = cursor.fetchall()
    connection.close()
    return calls

@app.route('/download_stations_csv')
def download_stations_csv():
    calls = list_table_content()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(["callsign","name","locator","bands","modes","schedule","comment","last_checkin"])
    cw.writerows(calls)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=ewn_stations.csv"
    output.headers["Content-type"] = "text/csv"
    return output
    
@app.route('/map_content')
def map_content():
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    cursor.execute("SELECT callsigns,locator FROM checkins;")
    calls = cursor.fetchall()
    connection.close();
    calls = [(i, mh.to_location(j, center=True)) for i,j in calls]
    ret_val = [{"type":"Point","coordinates":[j[1],j[0]], "icon": {"className": "c", "html":"<b class='c'>%s</b>"%i }} for i,j in calls]
    return render_template('map.html', entries=json.dumps(ret_val))
 

if __name__ == '__main__':
    app.run(threaded=True)
