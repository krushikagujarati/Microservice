# Product Microservice

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

# Initialize Flask app for Product service
product_app = Flask(__name__)
product_app.secret_key = "product_secret_key"
PRODUCT_DB = "product_service.db"

# Initialize SQLite database for Product service
def init_product_db():
    with sqlite3.connect(PRODUCT_DB) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, description TEXT)")
        con.commit()

# Product Service routes
@product_app.route('/', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        with sqlite3.connect(PRODUCT_DB) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO products (name, description) VALUES (?, ?)", (name, description))
            con.commit()
            flash("Product added successfully!")
            return redirect(url_for('products'))
    else:
        with sqlite3.connect(PRODUCT_DB) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM products")
            products = cur.fetchall()
        return render_template('products.html', products=products)

@product_app.route('/delete_product/<int:id>', methods=['GET'])
def delete_product(id):
    with sqlite3.connect(PRODUCT_DB) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM products WHERE id=?", (id,))
        con.commit()
        flash("Product deleted successfully!")
    return redirect(url_for('products'))

# Initialize the SQLite database for Product service
init_product_db()

# Note: The app isn't running yet. We'll provide instructions for running both microservices next.
