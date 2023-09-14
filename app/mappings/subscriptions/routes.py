import os

import stripe
from dotenv import load_dotenv
from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user

from database import get_db_connection

load_dotenv()

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
subscriptions_bp = Blueprint('subscriptions', __name__)


@subscriptions_bp.route('/plans')
def view_plans():
    return render_template('member-portal/subscriptions/plans.html')


@subscriptions_bp.route('/subscription_details')
def view_subscription_page():
    return render_template('member-portal/subscriptions/subscription_details.html')


@subscriptions_bp.route('/success')
def success():
    flash('Payment successful!')
    return render_template('member-portal/subscriptions/success.html')


@subscriptions_bp.route('/cancel')
def cancel():
    flash('Payment was cancelled.')
    return redirect(url_for('subscriptions.view_subscription_page'))


@subscriptions_bp.route('/choose_plan')
def choose_plan():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM plans")
    plans = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('member-portal/subscriptions/choose_plan.html', plans=plans)


@subscriptions_bp.route('/subscribe', methods=['POST'])
def subscribe():
    if not current_user.is_authenticated:
        flash("Please login to subscribe!")
        return redirect(url_for('auth.sign_in'))

    chosen_plan = request.form.get('plan')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT stripe_plan_id, stripe_price_id FROM plans WHERE plan_name=%s", (chosen_plan,))
    plan = cursor.fetchall()

    # Check if the user already has an active subscription for this plan
    cursor.execute("""
        SELECT subscriptions.id 
        FROM subscriptions 
        JOIN plans ON subscriptions.plan_id = plans.id 
        WHERE subscriptions.user_id = %s AND plans.plan_name = %s AND subscriptions.status = 'ACTIVE'
    """, (current_user.id, chosen_plan))

    existing_subscription = cursor.fetchone()

    if existing_subscription:
        flash('You already have an active subscription for this plan.')
        return redirect(url_for('subscriptions.view_subscription_page'))
    cursor.close()
    connection.close()

    # Using the same map to get the Stripe plan ID
    stripe_plan_id = plan[0]['stripe_plan_id']
    stripe_price_id = plan[0]['stripe_price_id']
    if not stripe_plan_id:
        flash('Invalid plan chosen!')
        return redirect(url_for('subscriptions.view_subscription_page'))

    try:
        # Create a Stripe Checkout session
        session = stripe.checkout.Session.create(
            customer=current_user.stripe_customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price': stripe_price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=url_for('subscriptions.success', _external=True) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=url_for('subscriptions.view_subscription_page', _external=True),
            client_reference_id=str(current_user.id),
        )

        # Redirect to Stripe Checkout
        return redirect(session.url)

    except Exception as e:
        flash(f"Error initiating Stripe checkout: {str(e)}")
        return redirect(url_for('subscriptions.view_subscription_page'))


# @subscriptions_bp.route('/view_subscriptions', methods=['GET'])
# def view_subscriptions():
#
#     connection = get_db_connection()
#     cur = connection.cursor(dictionary=True)
#     # Assuming you have a table called "subscriptions" which has the columns: user_id, start_date, end_date, price
#     cur.execute('''
#         SELECT users.full_name, users.email, subscriptions.start_date,
#                subscriptions.end_date, subscriptions.price
#         FROM users
#         JOIN subscriptions ON users.id = subscriptions.user_id
#     ''')
#
#     subscriptions = cur.fetchall()
#
#     return render_template('subscriptions.html', subscriptions=subscriptions)