from flask import Flask, request, redirect, url_for, abort, render_template_string, session, flash, get_flashed_messages
import hashlib
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simple in-memory user store
users = {
    'admin': {'password': 'password123password123', 'reset_token': None},
}

# Simulated in-memory database for reset tokens
reset_links = {}

# Home route
@app.route('/')
def home():
    if 'username' in session:
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Home</title>
                <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body { padding-top: 50px; }
                    .container { max-width: 500px; margin: auto; }
                    h1 { text-align: center; margin-bottom: 20px; }
                    p { text-align: center; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Welcome, {{ session["username"] }}</h1>
                    <p>You are logged in.</p>
                    <a href="/logout" class="btn btn-primary btn-block">Logout</a>
                </div>
            </body>
            </html>
        ''')
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Home</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { padding-top: 50px; }
                .container { max-width: 500px; margin: auto; }
                h1 { text-align: center; margin-bottom: 20px; }
                p { text-align: center; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome</h1>
                <p>You are not logged in.</p>
                <a href="/login" class="btn btn-primary btn-block">Login</a>
            </div>
        </body>
        </html>
    ''')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials! Please try again.')
            return redirect(url_for('login'))
    
    messages = get_flashed_messages()
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { padding-top: 50px; }
                .container { max-width: 500px; margin: auto; }
                form { margin-top: 20px; }
                .form-group { margin-bottom: 15px; }
                .btn { margin-top: 10px; }
                p { text-align: center; margin-top: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Login</h1>
                <script>
                    {% for message in messages %}
                        alert("{{ message }}");
                    {% endfor %}
                </script>
                <form method="POST">
                    <div class="form-group">
                        <label for="username">Username:</label>
                        <input type="text" name="username" id="username" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="password">Password:</label>
                        <input type="password" name="password" id="password" class="form-control">
                    </div>
                    <input type="submit" value="Login" class="btn btn-primary btn-block">
                </form>
                <p><a href="/forgot_password">Forgot Password?</a></p>
            </div>
        </body>
        </html>
    ''', messages=messages)

# Forgot Password route with alert
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        if username in users:
            curtime = str(int(time.time()))
            token = hashlib.md5(username.encode()).hexdigest() + "-" + curtime
            users[username]['reset_token'] = token
            reset_links[token] = username
            reset_link = url_for('reset_password', token=token, _external=True)
            print(reset_link)  # For debugging purposes
            flash(f'Reset token generated for {username} at {curtime}')
            flash("You should receive an email with the reset link: /reset_password/{token}")
            return redirect(url_for('forgot_password'))
        else:
            flash('User not found!')
            return redirect(url_for('forgot_password'))
    
    messages = get_flashed_messages()
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Forgot Password</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { padding-top: 50px; }
                .container { max-width: 500px; margin: auto; }
                form { margin-top: 20px; }
                .form-group { margin-bottom: 15px; }
                .btn { margin-top: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Forgot Password</h1>
                <script>
                    {% for message in messages %}
                        alert("{{ message }}");
                    {% endfor %}
                </script>
                <form method="POST">
                    <div class="form-group">
                        <label for="username">Enter your username:</label>
                        <input type="text" name="username" id="username" class="form-control">
                    </div>
                    <input type="submit" value="Reset Password" class="btn btn-primary btn-block">
                </form>
<!-- Don't tell anyone but the token generation is coded very poorly. The dev said it would be okay to use the following format for the password reset tokens: hashlib.md5(username.encode()).hexdigest() + "-" + str(int(time.time())) -->
            </div>
        </body>
        </html>
    ''', messages=messages)

# Dynamic Password Reset route
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if token not in reset_links:
        abort(404)
    
    if request.method == 'POST':
        new_password = request.form['password']
        username = reset_links[token]
        users[username]['password'] = new_password
        # Cleanup token
        del users[username]['reset_token']
        del reset_links[token]
        return redirect(url_for("login"))
    
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Password</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { padding-top: 50px; }
                .container { max-width: 500px; margin: auto; }
                form { margin-top: 20px; }
                .form-group { margin-bottom: 15px; }
                .btn { margin-top: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Reset Password</h1>
                <form method="POST">
                    <div class="form-group">
                        <label for="password">New Password:</label>
                        <input type="password" name="password" id="password" class="form-control">
                    </div>
                    <input type="submit" value="Reset Password" class="btn btn-primary btn-block">
                </form>
            </div>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
