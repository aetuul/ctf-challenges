from flask import Flask, request, redirect, render_template_string, session, url_for
import jinja2
import uuid

app = Flask(__name__)
app.secret_key = 'super-secret-key'

# In-memory report store
REPORTS = []

# Use a fresh Jinja2 environment manually for flexibility
jinja_env = jinja2.Environment()

@app.route('/')
def index():
    return '''
        <h2>Submit a Report</h2>
        <p>Powered by Flask and Jinja2</p>
        <form method="post" action="/report">
            <textarea name="content" rows="5" cols="50"></textarea><br>
            <button type="submit">Submit</button>
        </form>
        <br>
        <a href="/login">Admin Login</a>
    '''

@app.route('/report', methods=['POST'])
def report():
    content = request.form.get('content', '')
    REPORTS.append({
        'id': str(uuid.uuid4()),
        'content': content
    })
    return "Report submitted!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'supersecretadminpassword':
            session['admin'] = True
            return redirect(url_for('admin'))
        return 'Invalid credentials'
    return '''
        <h2>Admin Login</h2>
        <form method="post">
            Username: <input name="username" id="username"><br>
            Password: <input type="password" name="password" id="password"><br>
            <button type="submit" id="submit">Login</button>
        </form>
    '''

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('index'))

    output = "<h1>Admin Panel</h1><a href='/logout'>Logout</a><br><br>"
    for r in REPORTS:
        # 🚨 DELIBERATE BLIND SSTI: no autoescaping, user input compiled directly
        if "noscript" in r["content"].lower():
            r['content'] = r['content'].lower().replace("noscript", "")
        try:
            template = jinja_env.from_string(f"<noscript><div><b>Report:</b> {r['content']}</div></noscript><hr>")
            rendered = template.render()
            output += rendered
            
        except Exception as e:
            print(f"Error rendering report: {e}")
            output += f"<div>Error rendering report.</div><hr>"
            continue
    return output

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=9000)
