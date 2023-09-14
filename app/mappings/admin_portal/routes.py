import stripe
from flask import Blueprint, render_template, flash
from flask_jwt_extended import jwt_required
from flask_login import login_required

from app.models import User
from app.utilities import admin_required
from database import get_db_connection

admin_bp = Blueprint('admin_portal', __name__)


@admin_bp.route('/admin-portal', methods=['GET', 'POST'])
@jwt_required()
@admin_required
@login_required
def admin_portal():
    return render_template('/admin-portal/index.html')


@admin_bp.route('/admin-portal/view/users')
@jwt_required()
@admin_required
@login_required
def admin_portal_view_users():
    return render_template("admin-portal/view/users.html")


@admin_bp.route('/admin-portal/view/subscriptions')
@jwt_required()
@admin_required
@login_required
def admin_portal_view_payments():

    connection = get_db_connection()
    cur = connection.cursor(dictionary=True)
    # Assuming you have a table called "subscriptions" which has the columns: user_id, start_date, end_date, price
    cur.execute(''' 
        SELECT users.full_name, users.email, subscriptions.start_date, subscriptions.end_date, subscriptions.plan_id, p.plan_name, p.price
        FROM users
        JOIN subscriptions ON users.id = subscriptions.user_id
        JOIN plans p on subscriptions.plan_id = p.id
    ''')

    subscriptions = cur.fetchall()

    return render_template('admin-portal/view/subscriptions.html', subscriptions=subscriptions)


@admin_bp.route('/admin-portal/view/plans')
@jwt_required()
@admin_required
@login_required
def admin_portal_view_plans():
    return render_template("admin-portal/view/plans.html")


@admin_bp.route('/admin-portal/view/services')
@jwt_required()
@admin_required
@login_required
def admin_portal_view_services():
    return render_template("admin-portal/view/services.html")


@admin_bp.route('/admin-portal/edit/user/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
@login_required
def edit_user(user_id):
    db = get_db_connection()
    user = User.get_user_with_plan(db, user_id)
    if not user:
        return "User not found", 404  # or you can render a 404 page

    # Fetching subscription details from Stripe
    customer_subscriptions = None
    try:
        customer_subscriptions = stripe.Subscription.list(customer=user.stripe_customer_id)
        print("")
    except stripe.error.StripeError as e:
        flash(f"Error fetching Stripe details: {str(e)}", "danger")


    return render_template('admin-portal/edit/user.html', user=user, customer_subscriptions=customer_subscriptions)
