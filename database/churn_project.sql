USE regex;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    age INT,
    location VARCHAR(50),
    signup_date DATE,
    subscription_type VARCHAR(20)
);

CREATE TABLE payments (
    customer_id INT PRIMARY KEY,
    last_payment_date DATE,
    payment_delay_days INT,
    failed_payments_count INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE usage_metrics (
    customer_id INT PRIMARY KEY,
    avg_weekly_usage_hours DECIMAL(5,2),
    days_since_last_login INT,
    courses_completed INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE support_tickets (
    customer_id INT PRIMARY KEY,
    tickets_raised INT,
    last_ticket_days INT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);


