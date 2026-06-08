from flask import Flask, request, redirect, url_for, render_template
import os, sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, email TEXT, room TEXT, total_days INTEGER, total_price REAL)''')
    conn.commit()
    conn.close()

init_db()

# --- Room Prices ---
prices = {
    "Standard Room": 2499,
    "Deluxe Room": 4999,
    "Premium Room": 8999,
    "Family Suite": 16999,
    "Maharaja Suite": 32000
}

# --- Home Page ---
@app.route("/")
def home():
    return render_template("index.html")

# --- Upload Room Image ---
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["room_image"]
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
    return redirect(url_for("home"))

# --- Booking Route ---
@app.route("/book", methods=["POST"])
def book():
    name = request.form["name"]
    email = request.form["email"]
    room = request.form["room"]
    nights = int(request.form["nights"])
    days = int(request.form["days"])

    # Total stay duration
    total_stay = nights + days

    # Calculate price
    total_price = prices.get(room, 0) * total_stay

    # Save booking
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute("INSERT INTO bookings (name,email,room,total_days,total_price) VALUES (?,?,?,?,?)",
              (name, email, room, total_stay, total_price))
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))

# --- Dashboard ---
@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()
    conn.close()
    return render_template("dashboard.html", bookings=bookings)

# --- Delete Booking ---
@app.route("/delete/<int:booking_id>", methods=["POST"])
def delete(booking_id):
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

# --- Extend Booking ---
@app.route("/extend/<int:booking_id>", methods=["POST"])
def extend(booking_id):
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute("SELECT room,total_days FROM bookings WHERE id=?", (booking_id,))
    room, total_days = c.fetchone()
    total_days += 1
    new_price = prices[room] * total_days
    c.execute("UPDATE bookings SET total_days=?, total_price=? WHERE id=?",
              (total_days, new_price, booking_id))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

# --- Reduce Booking ---
@app.route("/reduce/<int:booking_id>", methods=["POST"])
def reduce(booking_id):
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute("SELECT room,total_days FROM bookings WHERE id=?", (booking_id,))
    room, total_days = c.fetchone()
    if total_days > 1:
        total_days -= 1
        new_price = prices[room] * total_days
        c.execute("UPDATE bookings SET total_days=?, total_price=? WHERE id=?",
                  (total_days, new_price, booking_id))
        conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
