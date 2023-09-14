import stripe
from flask import Blueprint, request, jsonify
from stripe.error import StripeError, InvalidRequestError

from database import get_db_connection

plans_blueprint = Blueprint('plans', __name__)


@plans_blueprint.route('/api/plans', methods=['GET'])
def get_all_plans():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM plans")
    plans = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(plans)


@plans_blueprint.route('/api/plans', methods=['POST'])
def add_new_plan():
    data = request.get_json()
    plan_name = data['plan_name']
    price = int(data['price'])
    services = data.get('services', [])

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        if not (0 <= price <= 999999):  # Assuming max price is 999999 of your base currency e.g. GBP
            return jsonify({"error": "Invalid price value"}), 400

        # Create Stripe product
        stripe_plan = stripe.Product.create(
            name=plan_name,
            description="Description for " + plan_name,
        )
        stripe_price = stripe.Price.create(
            product=stripe_plan.id,
            unit_amount=price * 100,
            currency='gbp',
            recurring={"interval": "month"},
        )

        # Insert into the database
        cursor.execute("INSERT INTO plans (plan_name, price, stripe_plan_id, stripe_price_id) VALUES (%s, %s, %s, %s)",
                       (plan_name, price, stripe_plan.id, stripe_price.id))
        plan_id = cursor.lastrowid

        # Insert associations between the new plan and the selected services
        for service_id in services:
            cursor.execute("INSERT INTO plan_services (plan_id, service_id) VALUES (%s, %s)", (plan_id, service_id))

        connection.commit()

    except StripeError as se:
        return jsonify({"error": f"Stripe error: {str(se)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 400
    finally:
        cursor.close()
        connection.close()

    return jsonify({"message": "Plan added successfully!"}), 201


@plans_blueprint.route('/api/plans/<int:plan_id>/services', methods=['GET'])
def get_plan_services(plan_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch services for a given plan
            sql = """
            SELECT services.id, services.service_name
            FROM services
            INNER JOIN plan_services ON services.id = plan_services.service_id
            WHERE plan_services.plan_id = %s
            """

            cursor.execute(sql, (plan_id,))
            services = cursor.fetchall()

        return jsonify(services), 200

    except Exception as e:
        # Log the exception for debugging
        print(e)
        return jsonify({"error": "Unable to fetch services for the plan"}), 500

    finally:
        connection.close()


@plans_blueprint.route('/api/plans/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch the stripe_plan_id for the plan
            cursor.execute("SELECT stripe_plan_id FROM plans WHERE id = %s", (plan_id,))
            plan = cursor.fetchone()

            if not plan:
                return jsonify({"error": "Plan not found"}), 404

            stripe_plan_id = plan[0]

            # First, delete the associations in the plan_services table
            cursor.execute("DELETE FROM plan_services WHERE plan_id = %s", (plan_id,))

            # Delete all subscriptions.
            cursor.execute("DELETE FROM subscriptions WHERE plan_id = %s", (plan_id,))

            # Now, delete the plan from the plans table
            cursor.execute("DELETE FROM plans WHERE id = %s", (plan_id,))

        connection.commit()
        return jsonify({"message": "Plan deleted successfully!"}), 200

    except InvalidRequestError as e:
        # This exception handles Stripe-related issues
        print(f"Stripe Error: {e}")
        return jsonify({"error": "Unable to delete the plan from Stripe"}), 500

    except Exception as e:
        # Log the exception for debugging
        print(e)
        return jsonify({"error": "Unable to delete the plan"}), 500

    finally:
        connection.close()