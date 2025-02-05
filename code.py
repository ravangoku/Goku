from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # VERY IMPORTANT: Change this to a random, complex string!

# Dummy data (replace with a database later)
items = {
    'books': [
        {'title': 'The Hitchhiker\'s Guide to the Galaxy', 'link': '#'},
        {'title': 'Pride and Prejudice', 'link': '#'},
    ],
    'hacking': [
        {'title': 'Hacking: The Art of Exploitation', 'link': '#'},
        {'title': 'Metasploit Unleashed', 'link': '#'},
    ],
    'misc': [
        {'title': 'Item 1', 'link': '#'},
        {'title': 'Item 2', 'link': '#'},
    ]
}


# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # In a real application, you would authenticate against a database
        if username == 'admin' and password == 'password':  # Example: Replace with database lookup
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/')
@login_required
def home():
    return render_template('home.html')


@app.route('/books')
@login_required
def books():
    return render_template('books.html', items=items['books'])


@app.route('/hacking')
@login_required
def hacking():
    return render_template('hacking.html', items=items['hacking'])


@app.route('/misc')
@login_required
def misc():
    return render_template('misc.html', items=items['misc'])


if __name__ == '__main__':
    app.run(debug=True)