#
# CREATE TABLE subscriptions (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     plan_id INT NOT NULL,
#     stripe_subscription_id VARCHAR(255) NOT NULL,
#     start_date DATE NOT NULL,
#     end_date DATE NOT NULL,
#     status ENUM('ACTIVE', 'CANCELLED', 'EXPIRED') NOT NULL,
#     FOREIGN KEY (user_id) REFERENCES users(id),
#     FOREIGN KEY (plan_id) REFERENCES plans(id)
# );
#
# ALTER TABLE users
# ADD COLUMN stripe_customer_id VARCHAR(255);



SELECT users.full_name, users.email, subscriptions.start_date, subscriptions.end_date, subscriptions.plan_id, p.plan_name, p.price
FROM users
JOIN subscriptions ON users.id = subscriptions.user_id
JOIN plans p on subscriptions.plan_id = p.id



SELECT users.id, users.full_name, users.email, subscriptions.plan_id, users.role, p.id, p.plan_name
                       FROM users
                       JOIN subscriptions ON users.id = subscriptions.user_id
                       JOIN plans p on subscriptions.plan_id = p.id WHERE id=28