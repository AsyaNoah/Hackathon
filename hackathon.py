mkdir online_booking_hackathon
cd online_booking_hackathon
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    booked = db.Column(db.Boolean, default=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    check_in = db.Column(db.String(80), nullable=False)
    check_out = db.Column(db.String(80), nullable=False)
    
    user = db.relationship('User', back_populates="bookings")
    room = db.relationship('Room', back_populates="bookings")

User.bookings = db.relationship('Booking', back_populates="user")
Room.bookings = db.relationship('Booking', back_populates="room")

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400
    
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": f"User {username} registered successfully!"}), 201

# Book a Room
@app.route('/book', methods=['POST'])
def book_room():
    data = request.get_json()
    user_id = data.get('user_id')
    room_id = data.get('room_id')
    check_in = data.get('check_in')
    check_out = data.get('check_out')

    room = Room.query.get(room_id)
    if room and not room.booked:
        room.booked = True
        booking = Booking(user_id=user_id, room_id=room_id, check_in=check_in, check_out=check_out)
        db.session.add(booking)
        db.session.commit()
        return jsonify({"message": f"Room {room.room_number} booked successfully!"}), 200
    return jsonify({"error": "Room is already booked or does not exist."}), 400

if __name__ == '__main__':
    app.run(debug=True)
python app.py
