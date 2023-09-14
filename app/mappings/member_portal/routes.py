from flask import Blueprint, render_template, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash

from app.forms import RegistrationForm
from database import get_db_connection

member_bp = Blueprint('member_portal', __name__)


@member_bp.route('/member-portal', methods=['GET', 'POST'])
@login_required
def member_portal():
    return render_template('/member-portal/index.html')


@member_bp.route('/member-portal/account/forgot-password')
def forgot_password():
    return render_template("auth/forgot_password.html")


@member_bp.route('/member-portal/account/register', methods=['GET', 'POST'])
def register_account():
    form = RegistrationForm()
    registration_successful = False
    already_exists = False
    if form.validate_on_submit():
        db = get_db_connection()
        cur = db.cursor()

        # Check if the email already exists in the database
        cur.execute("SELECT email FROM users WHERE email = %s", [form.data['email']])
        existing_user = cur.fetchone()
        # If the email is already taken
        if existing_user:
            flash('Account with that email already exists!', 'danger')
            already_exists = True
        else:
            # If email not taken, proceed with registration
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            cur.execute("INSERT INTO users (full_name, email, password, role) VALUES (%s, %s, %s, %s)",
                        (form.data['full_name'], form.data['email'], hashed_password, "USER"))
            db.commit()
            flash('You have successfully registered!', 'success')
            registration_successful = True

        cur.close()
    return render_template("auth/register.html", form=form,
                           registration_successful=registration_successful,
                           already_exists=already_exists)


@member_bp.route("/member-portal/refer-a-friend")
def refer_a_friend():
    return render_template("member-portal/refer-a-friend.html")
