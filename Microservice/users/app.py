# User Microservice

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

# Initialize Flask app for User service
user_app = Flask(__name__)
user_app.secret_key = "user_secret_key"
USER_DB = "user_service.db"

# Initialize SQLite database for User service
def init_user_db():
    with sqlite3.connect(USER_DB) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        con.commit()

# User Service routes
@user_app.route('/', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        name = request.form['name']
        with sqlite3.connect(USER_DB) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (name) VALUES (?)", (name,))
            con.commit()
            flash("User added successfully!")
            return redirect(url_for('users'))
    else:
        with sqlite3.connect(USER_DB) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
        return render_template('users.html', users=users)

@user_app.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
    with sqlite3.connect(USER_DB) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE id=?", (id,))
        con.commit()
        flash("User deleted successfully!")
    return redirect(url_for('users'))

# Initialize the SQLite database for User service
init_user_db()

# Note: The app isn't running yet. We'll provide instructions for running it after setting up the Product microservice.
