from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from authentication import Authentication

app = Flask(__name__)
app.secret_key = "92910"

auth = Authentication()

@app.route('/')
def home():
    if "user" not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user=session['user'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        result = auth.login_user(email, password)

        if result["SUCCESS"]:
            session["user"] = result["user"]
            return redirect(url_for('home'))
        return render_template('login.html', Error=result['MESSAGE'])
    return render_template('login.html')
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        result = auth.register_user(username, email, password)

        if result["SUCCESS"]:
            return redirect(url_for('login'))
        return render_template('register.html', Error=result['MESSAGE'])
    return render_template('register.html')

@app.route('/logout')
def logout(): 
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,  debug=True)