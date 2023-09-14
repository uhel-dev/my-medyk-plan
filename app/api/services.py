from flask import Blueprint, request, jsonify
from database import get_db_connection

services_blueprint = Blueprint('services', __name__)


@services_blueprint.route('/api/services', methods=['GET'])
def get_all_services():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(services)


@services_blueprint.route('/api/services', methods=['POST'])
def add_new_service():
    data = request.get_json()

    # First, validate the data. Check if the service name and price are provided
    if not data.get('service_name') or not data.get('price'):
        return jsonify({"message": "Service name and price are required!"}), 400

    service_name = data['service_name'].strip()  # Remove leading/trailing whitespaces
    price = data['price']

    connection = get_db_connection()
    cursor = connection.cursor()

    # Check for duplicates in the database
    cursor.execute("SELECT * FROM services WHERE service_name = %s", (service_name,))
    existing_service = cursor.fetchone()

    if existing_service:
        cursor.close()
        connection.close()
        return jsonify({"message": "Service with this name already exists!"}), 400

    # If there are no duplicates, proceed to insert the new service
    cursor.execute("INSERT INTO services (service_name, price) VALUES (%s, %s)", (service_name, price))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Service added successfully!"}), 201


@services_blueprint.route('/api/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Ensure service exists before deleting
    cursor.execute("SELECT * FROM services WHERE id = %s", (service_id,))
    service = cursor.fetchone()
    if not service:
        cursor.close()
        connection.close()
        return jsonify({"message": "Service not found!"}), 404

    cursor.execute("DELETE FROM services WHERE id = %s", (service_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Service deleted successfully!"}), 200