import pandas as pd
import numpy as np 
import mysql.connector
from src.config.db_config import DB_CONFIG # your dotenv config file


conn = mysql.connector.connect(**DB_CONFIG)

query = """
    SELECT 
    c.customer_id,
    c.age,
    c.location,
    c.signup_date,
    c.subscription_type,
    p.last_payment_date,
    p.payment_delay_days,
    p.failed_payments_count,
    u.avg_weekly_usage_hours,
    u.days_since_last_login,
    u.courses_completed,
    s.tickets_raised,
    s.last_ticket_days
    FROM customers c
    LEFT JOIN payments p ON c.customer_id = p.customer_id
    LEFT JOIN usage_metrics u ON c.customer_id = u.customer_id
    LEFT JOIN support_tickets s ON c.customer_id = s.customer_id
    """

df = pd.read_sql(query, conn)
conn.close()

# signup_date as numeric (days since signup)
df['signup_date'] = pd.to_datetime(df['signup_date'])
df['signup_date'] = (pd.Timestamp.today().normalize() - df['signup_date']).dt.days

# last_payment_date as numeric (days since last payment)
df['last_payment_date'] = pd.to_datetime(df['last_payment_date'])
df['last_payment_date'] = (pd.Timestamp.today().normalize() - df['last_payment_date']).dt.days


# Save to CSV
df.to_csv("customer_churn_dataset2.csv", index=False)

print("Dataset exported.")

# Convert to datetime
df['signup_date'] = pd.to_datetime(df['signup_date'])
df['last_payment_date'] = pd.to_datetime(df['last_payment_date'])

# Create numeric features
today = pd.Timestamp.today().normalize()

df['days_since_signup'] = (today - df['signup_date']).dt.days
df['days_since_last_payment'] = (today - df['last_payment_date']).dt.days

df = df.drop(columns=['signup_date', 'last_payment_date'])

#handling missing values
df['last_ticket_days'] = df['last_ticket_days'].fillna(0)

#creating the flag
df["payment_delay_flag"] = np.where(df["payment_delay_days"] > 7, 1, 0)
df["low_usage_flag"] = np.where(df["avg_weekly_usage_hours"] < 3, 1, 0)
df["support_intensity"] = df["tickets_raised"] / (df["courses_completed"] + 1)


df['engagement_rate'] = df['avg_weekly_usage_hours'] / (df['days_since_signup'] + 1)

df['activity_drop_flag'] = (df['days_since_last_login'] > 14).astype(int)


df['payment_stress'] = df['payment_delay_days'] * (df['failed_payments_count'] + 1)


df['support_pressure'] = df['tickets_raised'] / (df['days_since_signup'] + 1)




def handle_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    print(f"{column} → Lower: {lower_bound}, Upper: {upper_bound}")

    # Capping (not removing data)
    df[column] = df[column].apply(
        lambda x: lower_bound if x < lower_bound else upper_bound if x > upper_bound else x
    )

    return df


numeric_columns = [
    "age",
    "avg_weekly_usage_hours",
    "days_since_last_login",
    "courses_completed",
    "payment_delay_days",
    "failed_payments_count",
    "tickets_raised"
]

for col in numeric_columns:
    df = handle_outliers_iqr(df, col)

print("Outliers handled using IQR method!")

df=df.drop(columns='location')

df["churn"] = np.where(
    ((df["days_since_last_login"] > 30) & (df["failed_payments_count"] >= 1)) 
    | (df["avg_weekly_usage_hours"] < 2),
    1, 0
)

df.to_csv("processed_customer_data.csv", index=False)
print("Feature engineering done.")

