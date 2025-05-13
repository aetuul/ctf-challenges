import pickle
import base64
import os
import flask
from flask import request, make_response

app = flask.Flask(__name__)
app.secret_key = "super_secret_key"  # Needed for signing cookies

# Insecure function: Loads a pickle object from a cookie
def insecure_deserialize(data):
    try:
        return pickle.loads(base64.b64decode(data))  # Vulnerable
    except Exception as e:
        return f"Deserialization error: {e}"

@app.route('/')
def index():
    cookie = request.cookies.get('session')
    if cookie:
        result = insecure_deserialize(cookie)
        return f"""
        <h1>Sweet sour pickles 🥒</h1>
        <p>We've unpickled your session, and it says: <b>{result}</b></p>
        <p>Hope you didn't store anything... <i>explosive</i> in there.</p>
        <p><a href='/'>Refresh and try again?</a></p>
        """
    
    response = make_response("""
        <h1>Uh-oh! No session found! 🍪</h1>
        <p>Don't worry, we baked a fresh new cookie just for you.</p>
        <p>Try refreshing the page to see what happens!</p>
        """)
    safe_data = base64.b64encode(pickle.dumps({"user": "guest"})).decode()
    response.set_cookie('session', safe_data)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
