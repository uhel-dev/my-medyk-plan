import stripe
from flask import render_template, flash, redirect, url_for, make_response, g
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from flask_login import login_user, logout_user, current_user
from jwt import ExpiredSignatureError
from werkzeug.security import check_password_hash

from app import app, mysql, User
from app.forms import LoginForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(mysql.connection, form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            # User authentication successful, generate JWT token
            access_token = create_access_token(identity={"id": user.id, "role": user.role})

            # Set the token as a HttpOnly cookie for further API requests
            if user.role == "ADMIN":
                response = redirect(url_for('admin_portal.admin_portal'))
            else:
                response = redirect(url_for('member_portal.member_portal'))
            response.set_cookie('access_token_cookie', access_token, httponly=True)

            # Log in the user for Flask-Login's user management
            login_user(user, remember=True)

            # Check if user is logged in AND they already have a stripe_customer_id, if not create a Stripe customer for them
            if current_user.is_authenticated and not user.stripe_customer_id:
                customer = stripe.Customer.create(
                    email=user.email,
                    name=user.full_name
                )
                # Store the Stripe customer ID in your `users` table
                user.stripe_customer_id = customer.id

                # Update the stripe_customer_id in the database
                cur = mysql.connection.cursor()
                cur.execute("UPDATE users SET stripe_customer_id=%s WHERE id=%s", (customer.id, user.id))
                mysql.connection.commit()
                cur.close()

            return response
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('/auth/sign_in.html', form=form)


@app.route('/sign-out')
def sign_out():
    resp = make_response(redirect(url_for('index')))
    logout_user()  # This is for Flask-Login
    unset_jwt_cookies(resp)  # This clears the JWT cookies
    return resp


@app.before_request
def before_request():
    if current_user.is_authenticated:
        cur = mysql.connection.cursor()
        g.has_subscription = cur.execute("SELECT * FROM subscriptions WHERE user_id=%s", (current_user.id,)) > 0
    else:
        g.has_subscription = None


@app.errorhandler(ExpiredSignatureError)
def token_expired(e):
    # Redirecting to the sign-in page
    return redirect(url_for('sign_in'))
