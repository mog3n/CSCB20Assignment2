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
    d = getDb()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # find username password in both students and insturctors
        print(username, password)

        # TODO: Check DB for username and password
        p = (username,password)
        d.execute('SELECT * FROM S_login WHERE s_username=? AND s_password=?', p)
        student = d.fetchone()
        
        if student:
            (id, usr, pw) = student
            session['loggedin'] = True
            session['username'] = username
            session['type'] = "student"
            return redirect(url_for('home'))

        # check for teacher
        d.execute('SELECT * FROM T_login WHERE t_username=? AND t_password=?', p)
        teacher = d.fetchone()

        if teacher:
            (id, usr, pw) = teacher
            session['loggedin'] = True
            session['username'] = username
            session['type'] = "teacher"
            return redirect(url_for('home'))

        # else, return to login with eror message
        return render_template('login.html', error='Could not find a professor or student with those credentials.')

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
        username=session['username'],
        type=session['type'] # type: student or teacher
    )

@app.route('/studentPortal', methods=['GET'])
def grades():
    # ensure logged in
    if "loggedin" not in session:
        return render_template('login.html', error="Please login!")

    # ensure type is student
    if session['type'] != "student":
        return redirect(url_for('home'))

    username = session['username']
    p=(username,)
    d = getDb()
    
    marks = []
    for mark in d.execute('SELECT * FROM S_marks WHERE s_id=?', p):
        t_mark = {
            "s_username": mark[0],
            "course_name": mark[1],
            "assignment": mark[2],
            "grade": mark[3],
            "remark_request": mark[4]
        }

        marks.append(t_mark)

    # # Get grades for student
    # marks = [
    #         {
    #             "s_username": "Mogen",
    #             "course_name": "Gender Studies 1.0",
    #             "assignment": "Gender Analysis",
    #             "grade": 90,
    #             "remark_requested": False
    #         },
    #         {
    #             "s_username": "Mogen",
    #             "course_name": "Gender Studies 1.0",
    #             "assignment": "Midterm",
    #             "grade": 69,
    #             "remark_requested": True
    #         }
    #     ]
    
    profs = []
    for prof in d.execute('SELECT t_username FROM T_login'):
        profs.append(prof[0])

    username = session['username']
    return render_template('studentPortal.html', marks=marks, username=username, profs=profs)

@app.route('/addFeedback', methods=['POST'])
def addFeedback():
    if request.method == "POST":
        
        f1 = request.form['feedback1']
        s = request.form['s_username']
        t = request.form['t_username']
        # do some querying
        d = getDb()
        p = (s, t, f1)
    
        d.execute('INSERT INTO Feedback VALUES(?, ?, ?)', p)

        return redirect(url_for('studentPortal'))

@app.route('/')

@app.route('/updateGrade', methods=['POST'])
def updateGrade():
    grade = request.form['grade']
    student = request.form['s_username']
    assignment = request.form['assignment']



@app.route('/instructorPortal', methods=['GET'])
def allgrades():
    # ensure logged in
    if "loggedin" not in session:
        return render_template('login.html', error="Please login!")

    # ensure type is teacher
    if session['type'] != "teacher":
        return redirect(url_for('home'))

    d = getDb()
    feedbacks = []
    for feedback in d.execute('SELECT * FROM Feedback ORDER BY s_username'):
        feedbacks.append(feedback)
    print(feedback)

    d = getDb()
    marks = []
    for mark in d.execute('SELECT * FROM S_marks ORDER BY s_username'):
        marks.append(mark)
    print(marks)

    remarks = []
    for mark in marks:
        if mark['remark_requested'] == True:
            remarks.append(mark)

    return render_template('instructorPortal.html',
        feedback=feedback,
        marks=marks,
        remarks=remarks,
    )


if __name__ == '__main__':
    app.run(debug=True)
