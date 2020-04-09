from flask import Flask, render_template, request, url_for, redirect, session, send_from_directory, g
import sqlite3
app = Flask(__name__, template_folder="templates", static_url_path='', static_folder='static')
app.secret_key = "meme_reivew"

def getDb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db.cursor()

@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # find username password in both students and insturctors
        print(username, password)

        # TODO: Check DB for username and password
        

        session['loggedin'] = True
        session['username'] = username
        session['type'] = "student"

        # Greeting message
        if session['type'] == "student":
            session['greeting_message'] = "You can see your grades here"
        elif session['type'] == "teacher":
            session['greeting_message'] = "See my student grades"

        return redirect(url_for('home'))

    elif request.method == 'GET':
        
        c = getDb()
        for row in c.execute('SELECT * FROM S_login'):
            print(row)

        # check if logged in
        if "loggedin" in session:
            return redirect(url_for('home'))

        return render_template('login.html', msg='')


@app.route('/logout', methods=['GET'])
def logout():
    # not logged in
    if "loggedin" in session:
        # delete session
        session.pop('loggedin', None)

    return redirect(url_for('login'))
    

@app.route('/home', methods=['GET'])
def home():

    # ensure logged in
    if "loggedin" not in session:
        return render_template('login.html', error="Please login!")
    
    # otherwise show website
    return render_template('index.html',
        username=session['username'],
        greeting_message=session['greeting_message']
    )

@app.route('/marks', methods=['GET'])
def marks():
    # ensure logged in
    if "loggedin" not in session:
        return render_template('login.html', error="Please login!")
    
    # check type is a student
    if "student" not in session:
        return redirect(url_for('home'))
    
    # obtain classes and marks here

    

if __name__ == '__main__':
    app.run(debug=True)