from flask import Flask, render_template, request, url_for, redirect, session, send_from_directory
app = Flask(__name__, template_folder="templates", static_url_path='', static_folder='static')
app.secret_key = "meme_reivew"


@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # find username password in both students and insturctors
        print(username, password)

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
        username=session['username']
        
    )
    

if __name__ == '__main__':
    app.run(debug=True)