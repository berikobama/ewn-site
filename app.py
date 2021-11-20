import sqlite3
import psycopg2
import os
import io
import csv
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

if __name__ == '__main__':
    app.run(threaded=True)
