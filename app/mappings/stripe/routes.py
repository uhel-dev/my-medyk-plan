from datetime import datetime, timedelta

import stripe
from flask import current_app, Blueprint, request, jsonify, render_template

from database import get_db_connection

stripe_bp = Blueprint('stripe', __name__)


@stripe_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data.decode('utf-8')
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header,
                                               "whsec_41fae4251d4b858b88a02d898613219b36ec5c75e39f10054f4c30b315c594f3")
    except ValueError:
        # Invalid payload
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return jsonify({"error": "Invalid signature"}), 400

    # Handle the event
    if event.type == 'checkout.session.completed':
        session = event.data.object  # Get the session object
        # Handle the successful checkout, e.g., save to your database
        handle_successful_checkout(session)

        # Handle the event
    if event['type'] == 'customer.subscription.deleted':
        # Handle subscription deleted
        session = event.data.object
        handle_subscription_deleted(session)

    if event['type'] == 'product.deleted':
        session = event.data.object
        handle_product_delete(session)

    return jsonify({"success": True}), 200


def handle_successful_checkout(session):
    stripe_customer_id = session.customer  # Get the Stripe customer ID
    stripe_subscription_id = session.subscription  # Get the Stripe subscription ID

    # Fetch the subscription to get the associated price
    subscription = stripe.Subscription.retrieve(stripe_subscription_id)
    stripe_price_id = subscription.plan.stripe_id

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch user based on stripe_customer_id
    cursor.execute("SELECT id FROM users WHERE stripe_customer_id = %s", (stripe_customer_id,))
    user = cursor.fetchone()
    if not user:
        print("User not found.")
        return

    user_id = user['id']

    cursor.execute("SELECT id FROM plans WHERE stripe_price_id = %s", (stripe_price_id,))
    plan = cursor.fetchone()
    if not plan:
        print("Plan not found.")
        return

    plan_id = plan['id']

    # Assuming 30 days subscription for simplicity
    start_date = datetime.now().date()
    end_date = (start_date + timedelta(days=30 * 12))

    # Insert subscription details in your database
    cursor.execute(
        "INSERT INTO subscriptions (user_id, plan_id, stripe_subscription_id, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s, 'ACTIVE')",
        (user_id, plan_id, stripe_subscription_id, start_date, end_date)
    )
    connection.commit()
    cursor.close()

    return render_template('member-portal/subscriptions/success.html')


def handle_subscription_deleted(session):
    print("Subscription deleted.")


def handle_product_delete(session):
    # Delete the product from your database
    # Assuming you have a Product model with a stripe_product_id field
    plan_id = session.id
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id FROM plans WHERE stripe_plan_id = %s", (plan_id,))
    results = cursor.fetchall()

    for id in results:
        # First, delete the associations in the plan_services table
        cursor.execute("DELETE FROM plan_services WHERE plan_id = %s", (id,))

        # Delete all subscriptions.
        cursor.execute("DELETE FROM subscriptions WHERE plan_id = %s", (id,))

        # Now, delete the plan from the plans table
        cursor.execute("DELETE FROM plans WHERE id = %s", (id,))

    print(session)
