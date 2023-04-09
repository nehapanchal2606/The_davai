from flask import *
from flask_mysqldb import MySQL
import re
app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tha_davai_db'

mysql = MySQL(app)

@app.route('/', methods=['POST', 'GET'])
def index():
	cursor = mysql.connection.cursor()
	list_p = cursor.execute("SELECT * from product")
	list_product =  cursor.fetchall()
	print(list_product)
	cursor.execute("""CREATE TABLE IF NOT EXISTS bookingApointment (
		id INT auto_increment,
		name VARCHAR(255),
		email VARCHAR(255),	
		phone VARCHAR(255),
		appointment_date DATE,
		morning_desired BOOLEAN,
		afternoon_desired BOOLEAN,
		confirmation_requested_by VARCHAR(10),
		primary key (id)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS bookingApointment (
		id INT auto_increment,
		sale_person_name VARCHAR(255),
		no_products_sold INT,	
		sales_department VARCHAR(255),
		primary key (id)
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS bookingApointment (
		id INT auto_increment,
		sale_person_name VARCHAR(255),
		no_products_sold INT,	
		sales_department VARCHAR(255),
		primary key (id)
	)""")
	mysql.connection.commit()
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
	return render_template('index.html', list_product=list_product)

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
		#print('======? ',users[1]):
		if users:
			#print(" -- ",users[0]);
			# session['id'] = users[0]
			session['username'] = users[1]
			name = session['username']
			print("--",name)
			return redirect('/')
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
@app.route('/booking', methods=['GET','POST'])
def bookingAppointment():
	cursor = mysql.connection.cursor()
	if request.method == 'POST':
		
		name = request.form.get('name')
		email = request.form.get('email')
		phone = request.form.get('phone')
		appointment_date = request.form.get('Appointmentrequest')
		morning_desired = request.form.get('Morning desired')
		afternoon_desired = request.form.get('Afternoon desired')
		confirmation_requested_by = request.form.get('Confirmation requested by')
		cursor.execute('INSERT INTO user VALUES (%s,%s,%s,%s,%s,%s)',(username,city,contact,email,password))
		mysql.connection.commit()
		cursor.close()
		return 'Data added'

	return render_template('bookingAppointment.html', msg='')

@app.route('/about', methods=['GET'])
def aboute():
	return render_template('about.html', msg='')

@app.route('/contact', methods=['GET','POST'])
def contact():
	cursor = mysql.connection.cursor()
	if request.method == "POST":
    	# username = session['id']
		# print('username', username)
		cursor.execute()

		message = request.form.get()
		cursor.execute('INSERT INTO contact VALUES (%s,%s)',(username,message))

	return render_template('contact.html', msg='')

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


@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/shop')
def shop():
	cursor = mysql.connection.cursor()
	product_datas = cursor.execute('SELECT * from product')
	produst_lists = cursor.fetchall()
	print(produst_lists)
	return render_template('shop.html', produst_lists = produst_lists)

@app.route('/shop-detail/<int:id>',
methods=['GET','POST'])
def shop_detail(id):
	cursor = mysql.connection.cursor()
	get_product_detail = cursor.execute('SELECT * from product WHERE id=%s', (id,))
	Product_details = cursor.fetchone()
	print(Product_details,'-->')
	if request.method == 'POST':
		
		pro_qty = request.form.get('productQty')
		pro_id = request.form.get('id')
		print(pro_qty,pro_id,"=========>>>>")
	return render_template('shop-detail.html', Product_details = Product_details )
	
if __name__ == '__main__':
    app.run(debug=True)