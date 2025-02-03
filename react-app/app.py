from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Load MySQL connection details from environment variables
db_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),  # Docker service name or localhost
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'newpassword'),
    'database': os.getenv('MYSQL_DATABASE', 'crudnodejsmysql')
}

# Function to create a connection to the database
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Check database connectivity when the app starts
def check_db_connection():
    try:
        conn = get_db_connection()
        conn.close()
        print("Database connection successful. Your DB is up and fully accessible.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("Failed to connect to the database.")
        exit(1)

# Call the check_db_connection function when the app starts
check_db_connection()

# Root endpoint to show a welcome message when visiting the base URL
@app.route('/')
def index():
    return jsonify({"message": "Welcome! Your DB is up and fully accessible."})

# Endpoint to create a new customer
@app.route('/customer', methods=['POST'])
def create_customer():
    data = request.get_json()
    name = data['name']
    address = data['address']
    phone = data.get('phone', None)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO customer (name, address, phone) VALUES (%s, %s, %s)', (name, address, phone))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Customer created successfully!"}), 201

# Endpoint to get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM customer')
    customers = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(customers)

# Endpoint to get a customer by ID
@app.route('/customer/<int:id>', methods=['GET'])
def get_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM customer WHERE id = %s', (id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()

    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    return jsonify(customer)

# Endpoint to update a customer's details
@app.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    name = data.get('name', None)
    address = data.get('address', None)
    phone = data.get('phone', None)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE customer SET name = %s, address = %s, phone = %s WHERE id = %s', (name, address, phone, id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Customer updated successfully!"})

# Endpoint to delete a customer
@app.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM customer WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Customer deleted successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
