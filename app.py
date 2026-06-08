from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Ensure uploads folder exists
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database setup
def init_db():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    room_type TEXT NOT NULL,
                    nights INTEGER NOT NULL,
                    total_price INTEGER NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

# Room prices
ROOM_PRICES = {
    "standard": 2499,
    "deluxe": 4999,
    "premium": 8999,
    "family": 16999,
    "maharaja": 32000
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    email = request.form['email']
    room_type = request.form['room_type']
    nights = int(request.form['nights'])

    total_price = ROOM_PRICES[room_type] * nights

    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute("INSERT INTO bookings (name, email, room_type, nights, total_price) VALUES (?, ?, ?, ?, ?)",
              (name, email, room_type, nights, total_price))
    conn.commit()
    conn.close()

    return f"Booking confirmed for {name} ({email}) - {room_type} for {nights} nights. Total: ₹{total_price}"

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()
    conn.close()
    return render_template('dashboard.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)
