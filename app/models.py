from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, full_name, email, role, stripe_customer_id, plan_id=None, plan_name=None, password=None):
        self.id = id
        self.role = role
        self.email = email
        self.password = password
        self.full_name = full_name
        self.stripe_customer_id = stripe_customer_id
        self.plan_id = plan_id
        self.plan_name = plan_name

    @staticmethod
    def get(connection, user_id):
        cur = connection.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        data = cur.fetchone()
        cur.close()

        if data:
            return User(id=data[0], full_name=data[1], role=data[4], email=data[2], password=data[3],
                        stripe_customer_id=data[5])
        return None

    @staticmethod
    def get_by_email(connection, email):
        cur = connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        data = cur.fetchone()
        cur.close()

        if data:
            return User(id=data[0], full_name=data[1], role=data[4], email=data[2], password=data[3],
                        stripe_customer_id=data[5])
        return None

    @staticmethod
    def get_user_with_plan(connection, user_id):
        cur = connection.cursor()
        cur.execute("""SELECT users.id, users.full_name, users.email, users.stripe_customer_id, users.role, p.id, p.plan_name
                       FROM users
                       JOIN subscriptions ON users.id = subscriptions.user_id
                       JOIN plans p on subscriptions.plan_id = p.id
                       WHERE users.id=%s
                   """, (user_id,))
        data = cur.fetchone()
        cur.close

        if data:
            return User(id=data[0], full_name=data[1], email=data[2], stripe_customer_id=data[3], role=data[4], plan_id=data[5], plan_name=data[6])
        return None
