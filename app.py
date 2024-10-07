from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
import os
import time
import logging

app = Flask(__name__)
cors = CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure database
db_config = {
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'root'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('MYSQL_DATABASE', 'mydbc')
}

def get_db_connection(max_retries=5, delay_seconds=5):
    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                logger.info("Database connection successful")
                return conn
        except Error as e:
            logger.error(f"Database connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)
    
    logger.error("All database connection attempts failed")
    return None

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/check_db', methods=['GET'])
# def check_db():
#     conn = get_db_connection()
#     if conn:
#         conn.close()
#         return jsonify({"message": "Database connection successful"}), 200
#     else:
#         return jsonify({"message": "Database connection failed"}), 500

@app.route('/check_db', methods=['GET'])
def check_db():
    conn = get_db_connection()
    if conn:
        db_info = conn.get_server_info()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({
            "message": "Database connection successful",
            "db_info": db_info,
            "db_name": db_name
        }), 200
    else:
        return jsonify({"message": "Database connection failed"}), 500

        
@app.route('/add', methods=['POST'])
def add_data():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Failed to connect to the database"}), 500

    try:
        cursor = conn.cursor()
          # Ensure the users table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT
            )
        """)
        cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Data added successfully'})
    except Error as e:
        logger.error(f"Failed to add data: {str(e)}")
        return jsonify({"message": f"Failed to add data: {str(e)}"}), 500

@app.route('/display', methods=['GET'])
def display_data():
    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Failed to connect to the database"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Error as e:
        logger.error(f"Failed to fetch data: {str(e)}")
        return jsonify({"message": f"Failed to fetch data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')