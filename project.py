from flask import *
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tha_davai_db'

mysql = MySQL(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        firstName = request.form['firstname']
        lastName = request.form['lastname']
        cursor.execute("INSERT INTO userprofile(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        cursor.close()
        return 'Data added'
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)