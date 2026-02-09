Customer Churn Prediction System

A Machine Learning–based system designed to predict customers who are likely to discontinue a service. The project exposes real-time predictions through a FastAPI-based REST API, enabling integration with business systems.

Business Problem

Customer churn results in significant revenue loss. Organizations often identify churn only after a customer has already disengaged. This project focuses on early churn detection so that proactive retention strategies can be applied.

Churn Definition (Business Logic)

A customer is considered at risk of churn if:

No login activity for more than 30 days
and

Missed at least one payment
or

Very low service usage in the last 4 weeks

This combines behavioral inactivity, financial risk indicators, and declining engagement.

Project Objectives

Identify high-risk customers

Predict churn probability using Machine Learning

Provide predictions through an API

Support data-driven retention strategies

Key Features

Data preprocessing and feature engineering

Trained churn prediction model

REST API built using FastAPI

Modular, production-style code structure

Technology Stack

Python, FastAPI, Pandas, NumPy, Scikit-learn


API Endpoint

POST /predict
Accepts customer behavioral data and returns churn probability and prediction.

Business Impact

The system enables early identification of at-risk customers, helping organizations reduce churn, improve customer lifetime value, and make informed retention decisions.

Author

Vishakha Soni
Machine Learning and Data Science Enthusiast
