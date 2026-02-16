🚀 Customer Churn Predictor AI

An end-to-end AI-powered Customer Churn Prediction Web Application built for streaming platforms to identify at-risk customers and improve retention strategies using machine learning and analytics.

📌 Overview

Customer churn directly impacts revenue. This project provides a complete solution to:

Predict churn probability for individual customers

Perform bulk predictions on trained datasets

Track user prediction history

Provide actionable suggestions

Visualize analytics through dashboards

Export results for reporting

It combines Machine Learning + Full Stack Development + Business Analytics in one professional system.

✨ Features
🔍 Single Customer Prediction

Real-time churn probability calculation

Risk level classification (Low / Medium / High)

Visual probability progress bar

Intelligent suggestions based on risk

📊 Bulk Prediction

Run predictions on a dataset (ott_sample.csv)

Row-wise churn probability output

Risk categorization

Download results as CSV

👨‍💼 Admin Dashboard

Secure login access

View all customer prediction history

Analytics & churn trend visualization

Clear data functionality

Reporting support

👤 User Dashboard

Make churn predictions

View personal history

Analyze churn trends

📈 Analytics & Visualization

Interactive charts using Chart.js

Churn trends over time

Risk distribution insights

📁 Export Functionality

Export single & batch results as CSV

Useful for reporting and decision-making

🛠️ Tech Stack
Frontend

HTML5

CSS3 (Dark UI Design)

JavaScript

Chart.js

Backend

Python

Flask

Flask-CORS

Machine Learning

Scikit-learn

Joblib

Data Processing

Pandas

NumPy

🧠 Machine Learning Model

The model:

Uses customer behavioral & subscription features

Outputs churn probability using predict_proba()

Applies binary encoding for subscription types

Classifies churn risk based on probability threshold

📂 Project Structure
Customer-Churn-Predictor/
│
├── app.py
├── streaming_churn_model.pkl
├── ott_sample.csv
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── README.md

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/customer-churn-predictor.git
cd customer-churn-predictor

2️⃣ Create Virtual Environment (Optional but Recommended)
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt


If requirements.txt not available:

pip install flask flask-cors scikit-learn joblib pandas numpy

4️⃣ Run the Application
python app.py


Open in browser:

http://127.0.0.1:5000

📊 Example Input Features

Tenure (Months)

Average Watch Hours per Week

Days Since Last Login

Monthly Fee

Devices Used

Profiles Used

Support Tickets

Subscription Type

📈 Business Value

Helps reduce revenue loss

Enables proactive retention strategies

Identifies high-risk customers early

Supports data-driven decisions

Provides exportable insights for reporting

🔮 Future Improvements

User authentication with database

Cloud deployment (AWS / Azure)

Real-time database integration

Advanced ML models (XGBoost, Neural Networks)

Email alerts for high-risk customers

Role-based access control

👨‍💻 Author

Dhanush Mohan
3rd Year IT Student
Passionate about AI, Full Stack Development & Cloud Computing

📜 License

This project is open-source and available under the MIT License.

If you like this project, ⭐ star the repository and feel free to contribute!
