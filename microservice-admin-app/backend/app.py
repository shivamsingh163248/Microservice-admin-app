from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import time

app = Flask(__name__)
# Configure CORS to allow requests from frontend
CORS(app, origins=["http://localhost:8080", "http://127.0.0.1:8080", "http://frontend:80"])

# Function to connect to MySQL database with retries
def connect_to_database():
    max_retries = 30
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})")
            db = mysql.connector.connect(
                host=os.getenv("DB_HOST", "database"),
                user=os.getenv("DB_USER", "adminuser"),
                password=os.getenv("DB_PASS", "adminpass"),
                database=os.getenv("DB_NAME", "adminapp")
            )
            print("Successfully connected to database!")
            return db
        except mysql.connector.Error as e:
            print(f"Database connection failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Exiting.")
                raise e

# Global variables for database connection
db = None
cursor = None

def get_db_connection():
    global db, cursor
    if db is None:
        print("Initializing database connection...")
        db = connect_to_database()
        cursor = db.cursor()
    return db, cursor

@app.route('/register', methods=['POST'])
def register():
    try:
        db, cursor = get_db_connection()
        data = request.get_json()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (data['username'], data['password']))
        db.commit()
        return jsonify({"message": "Registration successful"})
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({"message": "Registration failed"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        db, cursor = get_db_connection()
        data = request.get_json()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (data['username'], data['password']))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"message": "Login failed"}), 500

@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if data['username'] == 'admin' and data['password'] == 'admin123':
        return jsonify({"message": "Admin Login successful"})
    else:
        return jsonify({"message": "Unauthorized"}), 401

@app.route('/users', methods=['GET'])
def get_users():
    try:
        db, cursor = get_db_connection()
        cursor.execute("SELECT username FROM users")
        users = [row[0] for row in cursor.fetchall()]
        return jsonify(users)
    except Exception as e:
        print(f"Get users error: {e}")
        return jsonify({"message": "Failed to fetch users"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        db, cursor = get_db_connection()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result:
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "message": "Database connection successful"
            })
    except Exception as e:
        print(f"Health check error: {e}")
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500

@app.route('/db-info', methods=['GET'])
def database_info():
    try:
        db, cursor = get_db_connection()
        
        # Get database version
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        
        # Get current database
        cursor.execute("SELECT DATABASE()")
        current_db = cursor.fetchone()[0]
        
        # Get tables in database
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Get user count
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        return jsonify({
            "database_version": version,
            "current_database": current_db,
            "tables": tables,
            "total_users": user_count,
            "connection_status": "success"
        })
    except Exception as e:
        print(f"Database info error: {e}")
        return jsonify({
            "error": str(e),
            "connection_status": "failed"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
