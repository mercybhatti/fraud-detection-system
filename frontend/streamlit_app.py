import os
import sqlite3
import hashlib
import requests
import time
import streamlit as st
from streamlit_cookies_controller import CookieController


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CONFIGURATION
# =========================================================

API_URL = "http://127.0.0.1:8000"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "users.db")

if "cookie_controller" not in st.session_state:
    st.session_state.cookie_controller = CookieController()

cookies = st.session_state.cookie_controller

# =========================================================
# DATABASE FUNCTIONS
# =========================================================

def get_database_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )

    connection.commit()
    return connection


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def register_user(username, password):
    connection = get_database_connection()

    try:
        connection.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, hash_password(password))
        )

        connection.commit()
        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "This username already exists."

    finally:
        connection.close()


def authenticate_user(username, password):
    connection = get_database_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT username
        FROM users
        WHERE username = ?
        AND password_hash = ?
        """,
        (username, hash_password(password))
    )

    user = cursor.fetchone()
    connection.close()

    return user is not None


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

        /* =================================================
           HIDE DEPLOY BUTTON AND STREAMLIT MENU
           KEEP HEADER VISIBLE FOR SIDEBAR TOGGLE
        ================================================= */

        /* Hide only Deploy button */
        [data-testid="stDeployButton"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* Hide Streamlit top-right menu */
        #MainMenu {
            display: none !important;
            visibility: hidden !important;
        }

        /* Hide footer */
        footer {
            display: none !important;
            visibility: hidden !important;
        }

        /* Keep Streamlit header visible */
        header {
            background: transparent !important;
            height: auto !important;
            min-height: 2.5rem !important;
            visibility: visible !important;
        }

        /* Keep header accessible */
        [data-testid="stHeader"] {
            background: transparent !important;
            height: auto !important;
            min-height: 2.5rem !important;
            visibility: visible !important;
            z-index: 999999 !important;
        }

        /* Keep sidebar open/close button visible */
        [data-testid="stSidebarCollapseButton"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
        }

        /* Keep header buttons accessible */
        [data-testid="stHeader"] button {
            visibility: visible !important;
            opacity: 1 !important;
        }


        /* =================================================
           MAIN APPLICATION BACKGROUND
        ================================================= */

        .stApp {
            background: #07111f;
        }


        /* =================================================
           SIDEBAR DESIGN
        ================================================= */

        section[data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #0c1b2e 0%,
                #081321 100%
            );

            border-right: 1px solid #20334b;
        }


        /* =================================================
           COMPACT SIDEBAR SPACING
        ================================================= */

        /* Sidebar overall padding */
        section[data-testid="stSidebar"] .block-container {
            padding-top: 0.4rem !important;
            padding-bottom: 0.3rem !important;
            padding-left: 1.25rem !important;
            padding-right: 1.25rem !important;
        }

        /* Sidebar markdown spacing */
        section[data-testid="stSidebar"] .stMarkdown {
            margin-top: 0 !important;
            margin-bottom: 0.05rem !important;
        }

        /* Paragraph spacing */
        section[data-testid="stSidebar"] p {
            margin-top: 0 !important;
            margin-bottom: 0.12rem !important;
            line-height: 1.25 !important;
        }

        /* Reduce spacing between sidebar elements */
        section[data-testid="stSidebar"] .element-container {
            margin-bottom: 0.15rem !important;
        }

        /* Sidebar title spacing */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            margin-top: 0.2rem !important;
            margin-bottom: 0.25rem !important;
        }


        /* =================================================
           CENTER SIGNED-IN STATUS BOX
        ================================================= */

        section[data-testid="stSidebar"] [data-testid="stAlert"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;

            padding: 0.45rem 0.7rem !important;
            margin-top: 0.2rem !important;
            margin-bottom: 0.2rem !important;

            border-radius: 8px !important;
        }

        section[data-testid="stSidebar"] [data-testid="stAlert"] p {
            width: 100% !important;
            text-align: center !important;
            margin: 0 !important;
        }


        /* =================================================
           COMPACT NAVIGATION RADIO BUTTONS
        ================================================= */

        section[data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 0 !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            min-height: 23px !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin: 0 !important;
        }


        /* =================================================
           SIDEBAR DIVIDERS
        ================================================= */

        section[data-testid="stSidebar"] hr {
            margin-top: 0.25rem !important;
            margin-bottom: 0.25rem !important;
        }


        /* =================================================
           SIDEBAR BUTTONS
        ================================================= */

        section[data-testid="stSidebar"] .stButton > button {
            min-height: 36px !important;
            padding: 0.25rem 0.5rem !important;
            border-radius: 10px !important;
        }


        /* =================================================
           CENTER API STATUS BOX
        ================================================= */

        section[data-testid="stSidebar"] [data-testid="stAlert"] {
            text-align: center !important;
        }

        section[data-testid="stSidebar"] [data-testid="stAlert"] div {
            text-align: center !important;
        }


        /* =================================================
           MAIN PAGE TITLE
        ================================================= */

        .main-title {
            font-size: 42px;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 4px;
        }

        .main-title span {
            color: #3b9cff;
        }

        .subtitle {
            font-size: 18px;
            color: #94a3b8;
            margin-bottom: 28px;
        }


        /* =================================================
           DASHBOARD CARDS
        ================================================= */

        .dashboard-card {
            background: linear-gradient(
                145deg,
                #122238,
                #0d1b2d
            );

            border: 1px solid #263c56;
            border-radius: 16px;
            padding: 24px;
            min-height: 125px;
            margin-bottom: 18px;
        }

        .card-heading {
            color: #f8fafc;
            font-size: 24px;
            font-weight: 700;
        }

        .card-description {
            color: #94a3b8;
            font-size: 15px;
            margin-top: 8px;
        }


        /* =================================================
           LOGIN PAGE
        ================================================= */

        .login-title {
            text-align: center;
            color: #f8fafc;
            font-size: 38px;
            font-weight: 800;
        }

        .login-subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 16px;
            margin-bottom: 25px;
        }

        .login-icon {
            text-align: center;
            font-size: 58px;
            margin-bottom: 8px;
        }


        /* =================================================
           GENERAL BUTTONS
        ================================================= */

        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            min-height: 44px;
        }


        /* =================================================
           METRICS
        ================================================= */

        [data-testid="stMetric"] {
            background: #122238;
            border: 1px solid #263c56;
            padding: 16px;
            border-radius: 12px;
        }

        /* =================================================
   API STATUS BOX — MATCH LOGOUT BUTTON
================================================= */

section[data-testid="stSidebar"] .api-status {
    width: 100% !important;
    height: 36px !important;
    box-sizing: border-box !important;

    margin: 0.4rem 0 0.5rem 0 !important;
    padding: 0 !important;

    border-radius: 10px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    text-align: center !important;
    font-size: 14px !important;
}

/* API Offline appearance */
section[data-testid="stSidebar"] .api-offline {
    background: #432936 !important;
    color: #ff6b6b !important;
}

/* API Ready appearance */
section[data-testid="stSidebar"] .api-ready {
    background: #123f36 !important;
    color: #4ade80 !important;
}

/* Logout button — exact same dimensions */
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    height: 36px !important;
    min-height: 36px !important;
    box-sizing: border-box !important;

    margin: 0 !important;
    padding: 0 !important;

    border-radius: 10px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    text-align: center !important;
}

/* =================================================
   SIGNED-IN BOX — FULL WIDTH AND CENTERED
================================================= */

section[data-testid="stSidebar"] .signed-in-box {
    width: 100% !important;
    height: 36px !important;
    box-sizing: border-box !important;

    margin: 0.4rem 0 0.5rem 0 !important;
    padding: 0 0.5rem !important;

    border-radius: 10px !important;
    background: #123f36 !important;
    color: #4ade80 !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    text-align: center !important;
    font-size: 14px !important;
}

/* =================================================
   LOGIN PAGE VIEWPORT SPACING
================================================= */

/* Reduce unnecessary top and bottom space on login page */
[data-testid="stAppViewContainer"] .main .block-container {
    padding-top: 0.8rem !important;
    padding-bottom: 0.5rem !important;
}

/* Keep login content compact */
.login-icon {
    margin-top: 0 !important;
    margin-bottom: 2px !important;
}

.login-title {
    margin-top: 0 !important;
    margin-bottom: 4px !important;
}

.login-subtitle {
    margin-top: 0 !important;
    margin-bottom: 12px !important;
}

/* Reduce spacing around login tabs */
div[data-testid="stTabs"] {
    margin-top: 0 !important;
}

/* Prevent unnecessary page-level vertical overflow */
[data-testid="stAppViewContainer"] .main {
    overflow-y: auto !important;
}


/* Sidebar branding */
section[data-testid="stSidebar"] .sidebar-brand {
    margin-top: -2.8rem !important;
    margin-bottom: 1.2rem !important;
}

section[data-testid="stSidebar"] .sidebar-brand-title {
    font-size: 28px;
    font-weight: 800;
    color: #f8fafc;
    white-space: nowrap;
    line-height: 1.2;
}

section[data-testid="stSidebar"] .sidebar-brand-subtitle {
    font-size: 15px;
    color: #94a3b8;
    margin-top: 8px;
    line-height: 1.2;
    text-align: center;

}

/* Move main dashboard content slightly upward */
[data-testid="stMainBlockContainer"] {
    padding-top: 1rem !important;
}

/* Compact prediction result cards */
.result-card,
.prediction-card,
.metric-card,
.result-panel {
    padding: 14px !important;
    margin-bottom: 10px !important;
}

.result-card h3,
.prediction-card h3,
.metric-card h3,
.result-panel h3 {
    margin-bottom: 6px !important;
}

.result-card p,
.prediction-card p,
.metric-card p,
.result-panel p {
    margin-bottom: 2px !important;
}

    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "logged_out" not in st.session_state:
    st.session_state.logged_out = False

# Restore authentication from browser cookies after refresh
browser_cookies = st.context.cookies

saved_authenticated = browser_cookies.get("authenticated")
saved_username = browser_cookies.get("username")

if (
    not st.session_state.logged_out
    and saved_authenticated in ("true", True, 1, "1")
    and saved_username
):
    st.session_state.authenticated = True
    st.session_state.username = saved_username

# =========================================================
# LOGIN AND SIGNUP PAGE
# =========================================================

def show_authentication_page():


    left_space, auth_column, right_space = st.columns(
        [1, 1.15, 1]
    
    )

    with auth_column:

        st.markdown(
            '<div class="login-icon">🛡️</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-title">Fraud Detection</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-subtitle">'
            'Secure access to your AI-powered fraud analysis dashboard'
            '</div>',
            unsafe_allow_html=True
        )

        login_tab, signup_tab = st.tabs(
            ["Sign In", "Create Account"]
        )

        # -------------------------------------------------
        # LOGIN
        # -------------------------------------------------

        with login_tab:

            with st.form("login_form"):

                username = st.text_input(
                    "Username",
                    placeholder="Enter your username"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                login_submitted = st.form_submit_button(
                    "Sign In",
                    use_container_width=True
                )

                if login_submitted:

                    if not username or not password:
                        st.warning(
                            "Please enter both username and password."
                        )

                    elif authenticate_user(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.logged_out = False

                        cookies.set("authenticated", "true", max_age=7 * 24 * 60 * 60)
                        cookies.set("username", username, max_age=7 * 24 * 60 * 60)

                        time.sleep(1)
                        st.rerun()

                    else:
                        st.error(
                            "Invalid username or password."
                        )

        # -------------------------------------------------
        # SIGN UP
        # -------------------------------------------------

        with signup_tab:

            with st.form("signup_form"):

                new_username = st.text_input(
                    "Choose Username",
                    placeholder="Create a username"
                )

                new_password = st.text_input(
                    "Create Password",
                    type="password",
                    placeholder="Create a strong password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter your password"
                )

                signup_submitted = st.form_submit_button(
                    "Create Account",
                    use_container_width=True
                )

                if signup_submitted:

                    if not new_username or not new_password:
                        st.warning(
                            "Please fill in all required fields."
                        )

                    elif len(new_username) < 3:
                        st.warning(
                            "Username must contain at least 3 characters."
                        )

                    elif len(new_password) < 6:
                        st.warning(
                            "Password must contain at least 6 characters."
                        )

                    elif new_password != confirm_password:
                        st.error(
                            "Passwords do not match."
                        )

                    else:
                        success, message = register_user(
                            new_username,
                            new_password
                        )

                        if success:
                            st.success(message)

                            st.info(
                                "Your account is ready. "
                                "Please open the Sign In tab."
                            )

                        else:
                            st.error(message)


# =========================================================
# API HEALTH CHECK
# =========================================================

def check_api_health():

    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )

        return response.status_code == 200

    except requests.exceptions.RequestException:
        return False


# =========================================================
# DASHBOARD
# =========================================================

def show_dashboard():

    # =====================================================
    # SIDEBAR
    # =====================================================

    with st.sidebar:

        st.markdown(
            '<div class="sidebar-brand"><div class="sidebar-brand-title">🛡️Fraud Detection</div><div class="sidebar-brand-subtitle">AI-powered risk analysis</div></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="signed-in-box">
                Signed in as: {st.session_state.username}
            </div>
            """,
            unsafe_allow_html=True
        )

        selected_page = st.radio(
            "Navigation",
            [
                "Home",
                "About",
                "Model Information",
                "API Status"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        st.markdown("### System Information")

        st.write("**Backend:** FastAPI")
        st.write("**Model:** XGBoost")
        st.write("**Task:** Binary Classification")
        st.write("**Purpose:** Fraud Detection")

        st.divider()

        if check_api_health():
            st.markdown(
                '<div class="api-status api-ready">API Ready</div>',
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                '<div class="api-status api-offline">API Offline</div>',
                unsafe_allow_html=True
            )    

        if st.button("Logout", use_container_width=True):

            # Prevent old browser cookies from restoring the dashboard
            st.session_state.logged_out = True
            st.session_state.authenticated = False
            st.session_state.username = ""

            # Expire browser authentication cookies
            cookies.set(
                "authenticated",
                "",
                max_age=0
            )

            cookies.set(
                "username",
                "",
                max_age=0
            )

            time.sleep(1.5)

            st.rerun()
    # =====================================================
    # HEADER
    # =====================================================

    st.markdown(
        '<div class="main-title">'
        'Fraud <span>Detection System</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Detect fraudulent financial transactions with AI'
        '</div>',
        unsafe_allow_html=True
    )


    # ============================================================
    # ABOUT PAGE
    # ============================================================

    if selected_page == "About":

        st.header("About the System")

        st.write(
            """
            ### AI-Powered Fraud Detection

            This application is an end-to-end fraud detection system designed
            to analyze financial transactions and estimate their fraud risk
            using machine learning.

            The system accepts transaction details such as transaction type,
            transaction amount, account balances, and fraud-related indicators.

            It then sends the information to a FastAPI backend, where the trained
            XGBoost classification model analyzes the transaction and returns
            a fraud probability, risk level, and final decision.
            """
        )

        st.markdown("### Key Features")

        st.markdown(
            """
            - Real-time transaction risk analysis
            - Machine learning-based fraud prediction
            - Fraud probability estimation
            - Risk classification: Low, Medium, or High
            - Fraudulent or Legitimate transaction decision
            - FastAPI backend integration
            - Interactive Streamlit user interface
            - Secure user authentication
            """
        )

        st.markdown("### Technology Stack")

        st.markdown(
            """
            - **Frontend:** Streamlit
            - **Backend:** FastAPI
            - **Machine Learning Model:** XGBoost Classifier
            - **Programming Language:** Python
            - **Dataset:** PaySim Financial Transaction Dataset
            - **Task:** Binary Classification
            """
        )

        st.info(
            "This system is intended to support fraud risk analysis and "
            "should be used as a decision-support tool."
        )

        return


    # ============================================================
    # MODEL INFORMATION PAGE
    # ============================================================

    if selected_page == "Model Information":

        st.header("Model Information")

        st.info("Model: XGBoost Classifier")

        st.markdown("### Model Overview")

        st.write(
            """
            The system uses an XGBoost Classifier to identify potentially
            fraudulent financial transactions.

            XGBoost is a gradient boosting algorithm that combines multiple
            decision trees to improve prediction performance.
            """
        )

        st.markdown("### Machine Learning Task")

        st.write("**Task:** Binary Classification")

        st.write(
            """
            The model predicts whether a transaction is:

            - **0:** Legitimate Transaction
            - **1:** Fraudulent Transaction
            """
        )

        st.markdown("### Model Output")

        st.markdown(
            """
            The model provides the following outputs:

            - Fraud probability
            - Risk level
            - Final transaction decision
            """
        )

        st.markdown("### Decision Threshold")

        st.write("**Decision Threshold:** 0.95")

        st.caption(
            "The decision threshold is used to convert the predicted fraud "
            "probability into a final fraud or legitimate decision."
        )

        st.markdown("### Model Features")

        st.markdown(
            """
            The model analyzes transaction-related features such as:

            - Transaction type
            - Transaction amount
            - Origin account balance
            - Destination account balance
            - Previous and updated account balances
            - Fraud flag indicator
            - Transaction step
            """
        )

        return


    # ============================================================
    # API STATUS PAGE
    # ============================================================

    if selected_page == "API Status":

        st.header("API Status")

        st.markdown("### Backend Connectivity")

        if check_api_health():

            st.success(
               "FastAPI backend is running successfully."
            )

            st.markdown(
                """
                **Backend Status:** Online  
                **API Framework:** FastAPI  
                **Health Endpoint:** `/health`  
                **Prediction Endpoint:** `/predict`  
                **Communication:** Streamlit → FastAPI
                """
            )

            st.info(
                "The frontend is successfully connected to the backend "
                "and is ready to process transaction predictions."
            )

        else:

            st.error(
                "FastAPI backend is not reachable."
            )

            st.warning(
                """
                Please make sure the Uvicorn server is running.

                Start the backend using:

                `uvicorn app.main:app --reload`
                """
            )

        return


    # =====================================================
    # MAIN HOME PAGE
    # =====================================================

    left_column, right_column = st.columns(
        [1.35, 1],
        gap="large"
    )


    # =====================================================
    # TRANSACTION FORM
    # =====================================================

    with left_column:

        st.markdown(
            """
        <div class="dashboard-card">
            <div class="card-heading">
                🧾 Enter Transaction Details
            </div>
            <div class="card-description">
                Provide transaction information to analyze fraud risk.
            </div>
        </div>
        """,
            unsafe_allow_html=True
        )

        with st.form("transaction_form"):

            col1, col2 = st.columns(2)

            with col1:

                step = st.number_input(
                    "Step",
                    min_value=0,
                    value=1,
                    step=1
                )

                amount = st.number_input(
                    "Transaction Amount",
                    min_value=0.0,
                    value=1000.0,
                    step=100.0
                )

                old_balance_org = st.number_input(
                    "Origin Account - Old Balance",
                    min_value=0.0,
                    value=5000.0,
                    step=100.0
                )

                new_balance_orig = st.number_input(
                    "Origin Account - New Balance",
                    min_value=0.0,
                    value=4000.0,
                    step=100.0
                )

            with col2:

                transaction_type = st.selectbox(
                    "Transaction Type",
                    options=[
                        "CASH_IN",
                        "CASH_OUT",
                        "DEBIT",
                        "PAYMENT",
                        "TRANSFER"
                    ]
                )

                old_balance_dest = st.number_input(
                    "Destination Account - Old Balance",
                    min_value=0.0,
                    value=2000.0,
                    step=100.0
                )

                new_balance_dest = st.number_input(
                    "Destination Account - New Balance",
                    min_value=0.0,
                    value=3000.0,
                    step=100.0
                )

                flagged_fraud = st.selectbox(
                    "Flagged as Fraud by System",
                    options=[0, 1],
                    format_func=lambda value:
                    "No (0)" if value == 0 else "Yes (1)"
                )

            submitted = st.form_submit_button(
                "🔍 Analyze Transaction",
                use_container_width=True
            )


    # =====================================================
    # PREDICTION RESULT
    # =====================================================

    with right_column:

        st.markdown(
            """
        <div class="dashboard-card">
            <div class="card-heading">
                📊 Prediction Result
            </div>
            <div class="card-description">
                AI analysis of the transaction risk.
            </div>
        </div>
        """,
            unsafe_allow_html=True
        )

        if not submitted:

            st.info(
                "Enter transaction details and click "
                "'Analyze Transaction' to get the fraud prediction."
            )

        if submitted:

            transaction_data = {
                "step": step,
                "type": transaction_type,
                "amount": amount,
                "oldbalanceOrg": old_balance_org,
                "newbalanceOrig": new_balance_orig,
                "oldbalanceDest": old_balance_dest,
                "newbalanceDest": new_balance_dest,
                "isFlaggedFraud": flagged_fraud
            }

            try:

                with st.spinner("Analyzing transaction..."):

                    response = requests.post(
                        f"{API_URL}/predict",
                        json=transaction_data,
                        timeout=30
                    )

                if response.status_code == 200:

                    result = response.json()

                    fraud_prediction = result["fraud_prediction"]
                    fraud_probability = result["fraud_probability"]
                    risk_level = result["risk_level"]
                    decision = result["decision"]

                    if fraud_prediction == 1:

                        st.error(
                            "🚨 Fraudulent Transaction Detected"
                        )

                    else:

                        st.success(
                            "✅ Transaction Appears Legitimate"
                        )

                    st.metric(
                        "Fraud Probability",
                        f"{fraud_probability * 100:.2f}%"
                    )

                    st.metric(
                        "Risk Level",
                        risk_level
                    )

                    st.metric(
                        "Decision",
                        decision
                    )
                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

                    try:
                        response.json()

                    except ValueError:
                        pass

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to FastAPI. "
                    "Please make sure the backend server is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. Please try again."
                )

            except requests.exceptions.RequestException as error:

                st.error(f"Request failed: {error}")


    st.divider()

    st.caption(
        "Fraud Detection System | FastAPI + XGBoost + Streamlit"
    )


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

if st.session_state.authenticated:
    show_dashboard()
else:
    show_authentication_page()