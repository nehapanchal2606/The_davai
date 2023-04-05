from flask import *
from flask_mysqldb import MySQL
import re
app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'the_davai_db'

mysql = MySQL(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        
        username = request.form.get('username')
        city = request.form.get('city')
        contact = request.form.get('contact')
        email = request.form.get('email')
        password = request.form.get('password')
        cursor.execute('INSERT INTO user VALUES (%s,%s,%s,%s,%s,%s)',(username,city,contact,email,password))
        mysql.connection.commit()
        cursor.close()
        return 'Data added'
    
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
	name = ''
	if request.method == 'POST':
		cursor = mysql.connection.cursor()
		username = request.form.get('username')
		password = request.form.get('password')
		#print('======>> ',username, password);
		#cur = mysql.connection.cursor(MySQLdb.cursors.DictCufrom flask import Flask,render_template,request,session,url_for,redirectrsor)
		cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username,password,))
		users = cursor.fetchone()
		#print('======? ',users[1]);


		
		if users:
			#print(" -- ",users[0]);
			# session['id'] = users[0]
			session['username'] = users[1]
			name = session['username']
			print("--",name)
			return render_template('index.html',name=name)
		else:
			msg = 'Incorrect username/password.'
		

		return render_template('login.html',msg=msg)

	if 'id' in session:
		return redirect('home')


	return render_template('login.html', msg='')


@app.route('/logout', methods=['GET'])
def logout():
	del session['id']
	del session['username']

	return redirect('/')

@app.route('/register',methods=['GET','POST'])
def register():
	msg=''
	
	if request.method == 'POST':
		cursor = mysql.connection.cursor()
		username = request.form.get('username')
		#birthdate = request.form.get('birthdate')
		city = request.form.get('city')
		contact = request.form.get('contact')
		email = request.form.get('email')
		password = request.form.get('password')

		#cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE username = %s',(username,))
		users = cursor.fetchone()

		if users:
			msg = 'User account exist!'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'username contain only character and numbers.'
		elif not username or not email or not password:
			msg = 'Please fill the form.'
		else:
			cursor.execute('INSERT INTO user (username, city, contact, email, password) VALUES (%s,%s,%s,%s,%s)', (username, city, contact, email, password))
			mysql.connection.commit()
			# cursor.commit()
			msg = 'Successfully Registered...'
			return render_template('login.html') 

	elif request.method == 'POST':
		msg = 'Please fill!'
	return render_template('register.html',msg=msg) 


if __name__ == '__main__':
    app.run(debug=True)