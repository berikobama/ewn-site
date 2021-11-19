import sqlite3
import psycopg2
import os
from flask import Flask
from flask import render_template

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
    cursor.execute("SELECT * FROM checkins;")
    calls = cursor.fetchall()
    connection.close()
    return calls

if __name__ == '__main__':
    app.run(threaded=True)
