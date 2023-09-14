from flask import Blueprint, request, jsonify, redirect, url_for
from flask_jwt_extended import jwt_required
from jwt import ExpiredSignatureError

from app.utilities import admin_required
from database import get_db_connection

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/api/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE role = %s", ("USER",))
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(users)


@users_blueprint.route('/api/users/<int:user_id>/plans', methods=['GET'])
def get_user_plans(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT plans.id, plans.plan_name, plans.price 
    FROM plans 
    JOIN user_plans ON plans.id = user_plans.plan_id 
    WHERE user_plans.user_id = %s
    """

    cursor.execute(query, (user_id,))
    user_plans = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(user_plans)


@users_blueprint.route('/api/users/<int:user_id>/plans', methods=['POST'])
def assign_plan_to_user(user_id):
    data = request.get_json()
    plan_id = data['plan_id']

    connection = get_db_connection()
    cursor = connection.cursor()

    # First, check if the user-plan relationship already exists to prevent duplicate assignments
    cursor.execute("SELECT * FROM user_plans WHERE user_id=%s AND plan_id=%s", (user_id, plan_id))
    existing_relation = cursor.fetchone()

    if existing_relation:
        cursor.close()
        connection.close()
        return jsonify({"message": "Plan already assigned to user."}), 409  # 409 Conflict

    # If no existing relationship, create the new user-plan relationship
    cursor.execute("INSERT INTO user_plans (user_id, plan_id) VALUES (%s, %s)", (user_id, plan_id))
    connection.commit()

    cursor.close()
    connection.close()
    return jsonify({"message": "Plan assigned to user successfully!"}), 201


@users_blueprint.route('/api/users/<int:user_id>/plans/<int:plan_id>', methods=['DELETE'])
def deassign_plan_from_user(user_id, plan_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM user_plans WHERE user_id=%s AND plan_id=%s", (user_id, plan_id))

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return jsonify({"message": "Plan was not assigned to the user or does not exist."}), 404  # 404 Not Found

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Plan deassigned from user successfully!"}), 200


@users_blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Delete the user by ID
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))

    # Check if a user was actually deleted
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return jsonify({"message": "User not found."}), 404  # 404 Not Found

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "User deleted successfully!"}), 200


@users_blueprint.errorhandler(ExpiredSignatureError)
def token_expired(e):
    # Redirecting to the sign-in page
    return redirect(url_for('/sign_in'))