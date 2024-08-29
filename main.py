
from flask import Flask, render_template, request, redirect, url_for

import pymysql

app = Flask(__name__)

def getDBConnection():
    connection = pymysql.connect(
        host='127.0.0.1',         # Replace with your host, e.g., '127.0.0.1'
        user='root',     # Replace with your MySQL username
        password='ijklmnop582#', # Replace with your MySQL password
        database='LMP'  # Replace with your database name
    )
    return connection

@app.route('/', methods=["GET"])
def index():
    connection = getDBConnection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT * FROM usuarios")
        users = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        users = []
    finally:
        cursor.close()
        connection.close()

    return render_template('index.html', users=users)

@app.route('/', methods=['POST'])
def submit():
    firstName = request.form['name']
    lastName = request.form['lname']
    
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (name, lname) VALUES (%s,%s)", (firstName, lastName))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))    


if __name__ == "__main__":
    app.run()