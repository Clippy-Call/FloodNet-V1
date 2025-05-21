from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from functools import wraps
from flask import request, Response
from sms import send_sms

def check_auth(username, password):
    return username == 'loki' and password == 'yoursaviorishere'

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response(
                'Login required', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL,
        location TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    location = request.form['location']

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, phone, location) VALUES (?, ?, ?, ?)', (name, email, phone, location))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))
    except sqlite3.IntegrityError:
        return "Email already registered. Please try again with a different email."

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/admin/users')
@requires_auth
def admin_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall() 

    conn.close()
    return render_template('admin_user.html', users=users)

@app.route('/api/flood-alert', methods=['POST'])
def flood_alert():
    data = request.get_json()
    location = data.get('location')
    level = data.get('level')

    if not location or not level:
        return jsonify({'error': 'Missing location or level'}), 400

    # Connect to DB
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT phone FROM users WHERE location = ?", (location,))
    users = cursor.fetchall()
    conn.close()

    # Compose alert message
    alert_msg = f"🚨 Flood Alert! Water level at {location} is {level}cm. Please stay alert and take precautions."

    # Send SMS to each user
    for user in users:
        phone = user[0]
        send_sms(phone, alert_msg)

    return jsonify({"status": "Alerts sent", "recipients": len(users)}), 200



if __name__ == '__main__':
    init_db()
    app.run(debug=True)
