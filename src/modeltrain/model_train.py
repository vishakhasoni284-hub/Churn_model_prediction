import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import Pipeline 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("processed_customer_data.csv")

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OrdinalEncoder(categories=[["Monthly", "Yearly"]]),["subscription_type"])
    ],
    remainder="passthrough"  # keep numeric columns as-is
)

pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("rfc", RandomForestClassifier())
])

X = df.drop(columns=["churn","days_since_last_login","failed_payments_count","avg_weekly_usage_hours"])
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(X_test.iloc[0].tolist())
pipeline.fit(X_train, y_train)

pred = pipeline.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))

joblib.dump(pipeline, "customer_churn_model.pkl")

print("Model saved successfully!")


    




