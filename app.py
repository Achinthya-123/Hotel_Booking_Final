from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Room details dictionary
rooms = {
    "standard": {
        "name": "Standard Room",
        "capacity": "1-2 people",
        "price": 2499
    },
    "deluxe": {
        "name": "Deluxe Room",
        "capacity": "2-3 people",
        "price": 4999
    },
    "premium": {
        "name": "Premium Room",
        "capacity": "2-3 people",
        "price": 8999
    },
    "family": {
        "name": "Family Suite",
        "capacity": "4-6 people",
        "price": 16999
    },
    "maharaja": {
        "name": "Maharaja/Presidential Suite",
        "capacity": "6-8 people",
        "price": 32000
    }
}

# Store bookings in memory (for demo; in real app use database)
bookings = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/book", methods=["POST"])
def book_room():
    room_type = request.form.get("room_type")
    nights = int(request.form.get("nights", 1))
    customer_name = request.form.get("name", "Guest")

    if room_type in rooms:
        room = rooms[room_type]
        total_cost = room["price"] * nights
        booking = {
            "name": customer_name,
            "room": room["name"],
            "nights": nights,
            "total": total_cost
        }
        bookings.append(booking)
        return f"Booking successful! {customer_name} booked {room['name']} for {nights} night(s). Total cost: ₹{total_cost}"
    else:
        return "Invalid room selection."

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", bookings=bookings)

@app.route("/upload", methods=["POST"])
def upload_photo():
    room_type = request.form.get("room_type")
    photo = request.files.get("photo")

    if photo and room_type in rooms:
        filename = secure_filename(room_type + ".jpg")
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f"Photo uploaded successfully for {rooms[room_type]['name']}!"
    else:
        return "Upload failed. Please select a valid room and photo."

if __name__ == "__main__":
    app.run(debug=True)
