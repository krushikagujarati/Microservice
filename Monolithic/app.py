from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "secret_key"
DATABASE = "monolithic.db"



# Initialize SQLite database
def init_db():
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, description TEXT)")
        con.commit()


# User Service routes
@app.route('/', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        name = request.form['name']
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (name) VALUES (?)", (name,))
            con.commit()
            flash("User added successfully!")
            return redirect(url_for('users'))
    else:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
        return render_template('users.html', users=users)


@app.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE id=?", (id,))
        con.commit()
        flash("User deleted successfully!")
    return redirect(url_for('users'))


# Product Service routes
@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO products (name, description) VALUES (?, ?)", (name, description))
            con.commit()
            flash("Product added successfully!")
            return redirect(url_for('products'))
    else:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM products")
            products = cur.fetchall()
        return render_template('products.html', products=products)


@app.route('/delete_product/<int:id>', methods=['GET'])
def delete_product(id):
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM products WHERE id=?", (id,))
        con.commit()
        flash("Product deleted successfully!")
    return redirect(url_for('products'))


# Initialize the SQLite database
init_db()

# Note: We're not running the app here. We'll provide the UI templates next.
# Then, we'll run the app to demonstrate the monolithic structure.
