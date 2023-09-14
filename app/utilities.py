# In utilities.py

from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify, flash, redirect, url_for


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] != 'ADMIN':
            return jsonify({"msg": "Admins only!"}), 403
        return fn(*args, **kwargs)

    return wrapper


def check_if_user_already_subscribes(cursor, current_user, chosen_plan):
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
