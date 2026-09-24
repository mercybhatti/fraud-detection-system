# Production ML + Deep Learning Fraud Detection System

I built this project to understand how machine learning can be used to identify suspicious financial transactions. The application allows users to enter transaction details and receive a fraud probability, risk level, and final decision through an interactive dashboard.

The project combines a Streamlit frontend, FastAPI backend, data preprocessing pipeline, and a trained XGBoost classification model. My main focus was to move beyond a simple machine learning notebook and build a complete application where a trained model can be used through an API.

## Project Overview

Financial fraud detection is a challenging machine learning problem because fraudulent transactions are usually very small compared to legitimate transactions. A model must identify suspicious patterns without incorrectly flagging too many genuine transactions.

In this project, I developed a fraud detection application that analyzes transaction-related information and predicts whether a transaction is legitimate or potentially fraudulent. The result is displayed in the form of fraud probability, risk level, and final decision.

The application allows users to:

- Enter financial transaction details.
- Validate the entered information.
- Send transaction data to the backend.
- Generate fraud probability using a trained model.
- View the assigned risk level.
- Receive a final fraud detection decision.
- Use the prediction system through an interactive dashboard.

## Why I Built This Project

I wanted to work on a practical machine learning problem where model performance depends on more than just accuracy. Fraud detection helped me understand imbalanced classification, precision, recall, probability thresholds, and the importance of reducing false positives and false negatives.

I also wanted to understand how a machine learning model can be integrated into a real application using FastAPI and Streamlit instead of keeping the entire project limited to a Jupyter Notebook.

## Problem Statement

Digital payment platforms process a large number of transactions every day. Manually checking each transaction is difficult because transaction volumes are high, fraud cases are rare, and suspicious patterns can be complex.

The objective of this project is to build a machine learning-based system that analyzes transaction features and helps identify potentially fraudulent transactions. The system provides a prediction that can support further financial risk analysis.

## Dataset

For this project, I used the PaySim Synthetic Financial Dataset available on Kaggle.

Dataset source:

https://www.kaggle.com/ealaxi/paysim1

PaySim is a synthetic dataset that simulates mobile money transactions. It contains information about transaction types, transaction amounts, account balances, and fraud indicators.

The main columns used in the project include:

- `step` – Unit of time in the simulation.
- `type` – Type of transaction.
- `amount` – Amount involved in the transaction.
- `nameOrig` – Origin account identifier.
- `oldbalanceOrg` – Origin account balance before the transaction.
- `newbalanceOrig` – Origin account balance after the transaction.
- `nameDest` – Destination account identifier.
- `oldbalanceDest` – Destination account balance before the transaction.
- `newbalanceDest` – Destination account balance after the transaction.
- `isFraud` – Target variable indicating whether the transaction is fraudulent.
- `isFlaggedFraud` – Indicator showing whether the transaction was flagged as suspicious.

## Target Variable

The target variable used for classification is `isFraud`.

- `0` represents a legitimate transaction.
- `1` represents a fraudulent transaction.

The dataset is highly imbalanced because legitimate transactions significantly outnumber fraudulent transactions. Therefore, accuracy alone cannot properly explain the performance of a fraud detection model.

## Exploratory Data Analysis

During the exploratory data analysis phase, I focused on understanding the structure of the dataset, transaction categories, feature distributions, missing values, account balance behavior, and fraud distribution.

I also analyzed how fraud was distributed across different transaction types. The analysis showed that fraudulent transactions were mainly concentrated in transaction categories such as `TRANSFER` and `CASH_OUT`, while some other categories contained very few or no fraudulent examples.

These observations helped me understand the dataset and decide which features could be useful for model training.

## Machine Learning Workflow

The project follows a complete machine learning workflow:

1. Loading the dataset.
2. Understanding the dataset structure.
3. Performing exploratory data analysis.
4. Checking data quality and missing values.
5. Analyzing numerical and categorical features.
6. Splitting the data into training and testing sets.
7. Preprocessing the input features.
8. Handling class imbalance during model training.
9. Training the classification model.
10. Generating fraud probabilities.
11. Analyzing classification thresholds.
12. Evaluating the model using suitable metrics.
13. Saving the trained model and preprocessing pipeline.
14. Using the saved model through a FastAPI backend.

## Data Preprocessing

The project uses a preprocessing pipeline to prepare the data before passing it to the machine learning model.

Numerical features are standardized using a scaling technique. This helps bring numerical features into a comparable range.

The numerical features used in the model include:

- `step`
- `amount`
- `oldbalanceOrg`
- `newbalanceOrig`
- `oldbalanceDest`
- `newbalanceDest`
- `isFlaggedFraud`

The categorical feature used in the model is:

- `type`

The transaction type is converted into a machine-readable format using one-hot encoding.

The preprocessing pipeline ensures that the same transformations are applied during both model training and prediction. This helps maintain consistency between the training process and the live application.

## Handling Class Imbalance

Fraud detection datasets usually contain a very small percentage of fraudulent transactions. This creates a class imbalance problem because a model can achieve high accuracy by predicting most transactions as legitimate.

To address this issue, I used class-imbalance handling during model training. I also focused on evaluation metrics such as precision, recall, F1-score, ROC-AUC, and Precision-Recall AUC instead of depending only on accuracy.

These metrics provide a better understanding of how well the model identifies fraudulent transactions.

## Model Used

### XGBoost Classifier

The primary model used in this project is the XGBoost Classifier.

XGBoost is a gradient boosting algorithm that combines multiple decision trees to learn complex patterns in structured data. I selected XGBoost because it works well with tabular datasets and can capture non-linear relationships between features.

It is also useful for binary classification, probability-based predictions, and situations where feature interactions are important.

The model is trained to perform binary classification and predict whether a transaction is legitimate or fraudulent.

## Classification Task

This project is a binary classification problem.

The model predicts one of the following outcomes:

- Legitimate transaction
- Fraudulent transaction

Along with the final classification, the model also generates a probability score representing how likely the transaction is to be fraudulent.

## Model Input Features

The model uses the following transaction-related features:

- Transaction step
- Transaction type
- Transaction amount
- Origin account balance before the transaction
- Origin account balance after the transaction
- Destination account balance before the transaction
- Destination account balance after the transaction
- Fraud flag indicator

The categorical feature is encoded, and numerical features are scaled before being passed to the trained model.

## Model Evaluation
Because the dataset is highly imbalanced, I evaluated the model using metrics that are more meaningful for fraud detection.

### Precision
Precision measures how many transactions predicted as fraudulent were actually fraudulent. It helps understand how many false alerts are being generated by the model.

### Recall
Recall measures how many actual fraudulent transactions were successfully detected by the model. It is important because missing fraudulent transactions can lead to financial losses.

### F1-Score
F1-score combines precision and recall into a single metric. It is useful when both false positives and false negatives need to be considered.

### ROC-AUC
ROC-AUC measures the model's ability to distinguish between legitimate and fraudulent transactions across different classification thresholds.

### Precision-Recall AUC
Precision-Recall AUC is especially useful for imbalanced classification problems because it focuses more on the performance of the minority class.

## Threshold Optimization
A machine learning classification model generates a probability between 0 and 1. This probability must be converted into a final decision using a classification threshold.

For example, if the predicted fraud probability is greater than or equal to the selected threshold, the transaction is classified as fraudulent. Otherwise, it is classified as legitimate.

Instead of automatically using the default threshold, I analyzed different threshold values using precision, recall, and F1-score. This helped me understand the trade-off between detecting more fraudulent transactions and reducing false alerts.

The selected threshold is used by the application when generating the final transaction decision.

## Application Features
The application includes a user authentication interface where users can log in or create an account.

After logging in, users can access the fraud detection dashboard and enter transaction details. The frontend sends the transaction information to the FastAPI backend, where the input is validated and processed.

The application provides:

- User login and signup interface.
- Transaction input form.
- Input validation.
- FastAPI backend integration.
- Fraud probability prediction.
- Risk level classification.
- Final transaction decision.
- API health status.
- Interactive Streamlit dashboard.
- Separate information pages explaining the project and model.

## Prediction Output
For every analyzed transaction, the application displays three main results.

### Fraud Probability
This represents the estimated probability that the transaction is fraudulent.

### Risk Level
The transaction is assigned a risk level based on its predicted fraud probability.
The application uses the following risk categories:

- Low
- Medium
- High

### Final Decision
The final decision indicates whether the transaction is classified as:

- Legitimate
- Fraudulent

## Application Architecture
The application follows this flow:

User  
↓  
Streamlit Frontend  
↓  
Transaction Input Validation  
↓  
FastAPI Backend  
↓  
Preprocessing Pipeline  
↓  
Trained XGBoost Model  
↓  
Fraud Probability  
↓  
Risk Classification  
↓  
Final Prediction  
↓  
Streamlit Dashboard

The frontend is responsible for collecting user input and displaying results. The FastAPI backend handles request validation, preprocessing, model inference, and prediction response generation.

## Application Workflow

The user first opens the Streamlit application and logs in or creates an account. After authentication, the user enters transaction information through the prediction form.

The frontend validates the input and sends the transaction data to the FastAPI backend. The backend validates the request again, applies the preprocessing pipeline, and passes the processed features to the trained XGBoost model.

The model generates a fraud probability. The selected classification threshold is then applied to determine the final decision. The system assigns a risk level and sends the result back to the Streamlit frontend.

Finally, the prediction result is displayed on the dashboard.

## Project Structure

```text
fraud-detection-system/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   └── ...
│
├── data/
│   └── raw/
│       └── transactions.csv
│
├── frontend/
│   ├── streamlit_app.py
│   └── users.db
│
├── ml/
│   ├── notebooks/
│   ├── models/
│   ├── preprocessing/
│   └── ...
│
├── tests/
│
├── docs/
│
├── .gitignore
├── README.md
└── requirements.txt

Technologies Used:
The main technologies and tools used in this project include:

Python
Pandas
NumPy
Scikit-learn
XGBoost
FastAPI
Pydantic
Streamlit
SQLite
Jupyter Notebook
Matplotlib
Git and GitHub

Installation and Setup
1. Clone the Repository
--git clone <repository-url>
2. Navigate to the Project Directory
--cd fraud-detection-system
3. Create a Virtual Environment
--py -3.12 -m venv .venv
4. Activate the Virtual Environment
For Windows PowerShell:
--.\.venv\Scripts\Activate.ps1
5. Install Dependencies
--pip install -r requirements.txt

Running the Application

The application requires two services:
FastAPI backend
Streamlit frontend
Start the FastAPI Backend
Run the following command from the project root:
uvicorn app.main:app --reload

The backend will be available at:

http://127.0.0.1:8000
Start the Streamlit Frontend

Open another terminal, activate the virtual environment, and run:
--streamlit run .\frontend\streamlit_app.py

The Streamlit application will open in the browser.

API Endpoints

GET /health
This endpoint checks whether the FastAPI backend is running and available.

POST /predict
This endpoint accepts transaction details and returns the fraud prediction result.
The response includes information such as:
Fraud probability
Risk level
Final decision

Example Prediction Response
{
  "fraud_probability": 0.9994,
  "risk_level": "High",
  "decision": "Fraudulent"
}

The exact response values depend on the transaction details submitted to the model.

Application Testing

I tested the application using different transaction scenarios to check whether the model and API were working as expected.

Legitimate Transaction Test

I tested a normal CASH_IN transaction with regular account balance changes. The application returned a very low fraud probability, assigned a low risk level, and classified the transaction as legitimate.

Fraudulent Transaction Test

I also tested a suspicious TRANSFER transaction with a high transaction amount and unusual account balance behavior. The application returned a very high fraud probability, assigned a high risk level, and classified the transaction as fraudulent.

API Connectivity Test

The Streamlit frontend was connected successfully to the FastAPI backend. The API health status was displayed in the application, confirming that the frontend and backend were communicating properly.

Project Highlights

This project helped me apply machine learning concepts in a complete application rather than using them only for model training.

The major concepts covered in this project include:
Imbalanced binary classification
Exploratory data analysis
Numerical and categorical feature preprocessing
XGBoost classification
Probability-based predictions
Classification threshold optimization
REST API development
FastAPI integration
Streamlit dashboard development
Input validation
Frontend-backend communication
Model inference
Modular project organization
Challenges I Faced

One of the main challenges was working with a highly imbalanced dataset where fraudulent transactions were much fewer than legitimate transactions.

Another challenge was understanding how to evaluate the model using suitable metrics instead of focusing only on accuracy. I also worked on converting the trained model into an API-based prediction system and connecting it with a user-friendly frontend.

Integrating preprocessing, model prediction, API validation, and dashboard output helped me understand the complete flow of a machine learning application.

What I Learned

While building this project, I gained practical experience in preparing a real-world-style dataset, performing exploratory data analysis, handling class imbalance, training a classification model, and evaluating its performance.

I also learned how to use preprocessing pipelines, optimize classification thresholds, save trained machine learning components, and integrate a model with FastAPI and Streamlit.

This project improved my understanding of how machine learning models can be connected with software applications and used through a simple user interface.

Future Improvements
Some improvements that I may work on in the future include:
Adding deep learning-based fraud detection models.
Comparing multiple machine learning models.
Adding SHAP-based model explanations.
Storing transaction prediction history.
Adding model monitoring.
Implementing data drift detection.
Improving authentication persistence.
Adding Docker-based deployment.
Deploying the application on a cloud platform.
Adding production-grade logging.
Supporting real-time transaction monitoring.

Project Outcome
This project gave me hands-on experience in building an end-to-end machine learning application for financial transaction analysis.

By combining data analysis, model training, preprocessing, FastAPI, and Streamlit, I developed a system that accepts transaction information and provides a practical fraud risk prediction through an interactive interface.

The project helped me understand the complete journey of a machine learning solution, from dataset exploration and model development to API integration and application testing.