from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Connect to MySQL database
db = mysql.connector.connect(
    host="database",         # MUST match service name in docker-compose.yml
    user="root",
    password="password",
    database="adminapp"
)
cursor = db.cursor()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (data['username'], data['password']))
    db.commit()
    return jsonify({"message": "Registration successful"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (data['username'], data['password']))
    user = cursor.fetchone()
    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if data['username'] == 'admin' and data['password'] == 'admin123':
        return jsonify({"message": "Admin Login successful"})
    else:
        return jsonify({"message": "Unauthorized"}), 401

@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT username FROM users")
    users = [row[0] for row in cursor.fetchall()]
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
