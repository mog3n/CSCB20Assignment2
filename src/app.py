from flask import Flask, render_template, request, url_for, redirect, session, send_from_directory, g
import sqlite3
app = Flask(__name__, template_folder="templates", static_url_path='', static_folder='static')
app.secret_key = "meme_reivew"

def getDb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db

@app.route('/', methods=['GET', 'POST'])
def login():
    d = getDb().cursor()

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
            (usr, pw) = student
            session['loggedin'] = True
            session['username'] = username
            session['type'] = "student"
            return redirect(url_for('home'))

        # check for teacher
        d.execute('SELECT * FROM T_login WHERE t_username=? AND t_password=?', p)
        teacher = d.fetchone()

        if teacher:
            (usr, pw) = teacher
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

@app.route('/requestRemark', methods=['POST'])
def remarkRequest():
    if request.method == "POST":
        mark_name = request.form['mark_name']
        s_username = session['username']
        class_id = request.form['class_id']

        p = (s_username, mark_name, class_id)
        q = "UPDATE S_marks SET remark_request=1 WHERE s_username =? and mark_name=? and class_id=?"

        c = getDb().cursor()
        c.execute(q, p)
        getDb().commit()

        return redirect('/studentPortal')

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
    d = getDb().cursor()
    
    marks = []
    for mark in d.execute('SELECT * FROM S_marks WHERE s_username=?', p):
        marks.append(mark)

    profs = []
    for prof in d.execute('SELECT t_username FROM T_login'):
        profs.append(prof[0])

    username = session['username']
    return render_template('studentPortal.html', marks=marks, username=username, profs=profs)


@app.route('/addFeedback', methods=['POST'])
def addFeedback():
    if request.method == "POST":
        f1 = request.form['feedback']
        s = request.form['s_username']
        t = request.form['t_username']
        # do some querying
        d = getDb().cursor()
        p = (s, t, f1)
        
        q = "INSERT INTO Feedback values (?,?,?)"
        d.execute(q, p)
        getDb().commit()
        return redirect('/studentPortal')
    
    else:
        return redirect('/studentPortal')

@app.route('/')

@app.route('/updateGrade', methods=['POST'])
def updateGrade():

    if request.method == "POST":
        grade = request.form['grade']
        student = request.form['s_username']
        class_id = request.form['class_id']
        mark_name = request.form['mark_name']

        p = (grade, student, mark_name, class_id)
        q = "UPDATE S_marks SET grade=?, remark_request=0 WHERE s_username =? and mark_name=? and class_id=?"

        d = getDb().cursor()
        d.execute(q, p)
        getDb().commit()

        return redirect('/instructorPortal')
    else:
        return "You don't have permission lmao"


@app.route('/instructorPortal', methods=['GET'])
def allgrades():
    # ensure logged in
    if "loggedin" not in session:
        return render_template('login.html', error="Please login!")

    # ensure type is teacher
    if session['type'] != "teacher":
        return redirect(url_for('home'))

    # Get all feedback
    d = getDb().cursor()
    feedback_list = []
    for feedback in d.execute('SELECT * FROM Feedback'):
        feedback_list.append(feedback)
    print("Feedback")
    print(feedback_list)
    # Get all marks
    d = getDb().cursor()
    marks = []
    for mark in d.execute('SELECT * FROM S_marks ORDER BY s_username'):
        marks.append(mark)
    print("Marks")
    print(marks)
    # Get a list of remarks
    remarks = []
    for mark in marks:
        if mark[3] == 1:
            remarks.append(mark)

    return render_template('instructorPortal.html',
        feedback=feedback_list,
        marks=marks,
        remarks=remarks,
    )


if __name__ == '__main__':
    app.run(debug=True)
