from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['host']
app.config['MYSQL_USER'] = db['user']
app.config['MYSQL_PASSWORD'] = db['password']
app.config['MYSQL_DB'] = db['dbname']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        studentDetails = request.form
        rnum = studentDetails['rnum']
        name = studentDetails['nos']
        email = studentDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student_table(rnum, name, email) VALUES(%s, %s, %s)",(rnum, name, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/students')
    return render_template('index.html')

@app.route('/students')
def students():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM student_table")
    if resultValue > 0:
        studentDetails = cur.fetchall()
        return render_template('students.html',studentDetails=studentDetails)

if __name__ == '__main__':
    app.run(debug=True)
