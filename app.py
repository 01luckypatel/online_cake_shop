from flask import Flask, render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "server_secret_string"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cake_shop'
db = SQLAlchemy(app)

class accounts(db.Model):
	sno = db.Column(db.Integer,primary_key=True)
	emails = db.Column(db.String(100),nullable = False)
	passwords = db.Column(db.String(100),nullable = False)

class admin_accounts(db.Model):
	sno = db.Column(db.Integer,primary_key=True)
	emails = db.Column(db.String(100),nullable = False)
	passwords = db.Column(db.String(100),nullable = False)


class products(db.Model):
	sno = db.Column(db.Integer,primary_key=True)
	# product_id = db.Column(db.String(100),nullable = False)
	product_name = db.Column(db.String(100),nullable = False)
	product_price = db.Column(db.Integer,nullable = False)
	product_description = db.Column(db.String(100),nullable = False)

class cartitems(db.Model):
	sno = db.Column(db.Integer,primary_key=True)
	# product_id = db.Column(db.String(100),nullable = False)
	added_by = db.Column(db.String(100),nullable = False)
	product_id = db.Column(db.Integer,nullable = False)

	
# order_no 	product_id 	order_by 	time 	status 	address 

class orders(db.Model):
	order_no = db.Column(db.Integer,primary_key=True)
	product_id = db.Column(db.Integer,nullable = False)
	order_by  = db.Column(db.String(100),nullable = False)
	time = db.Column(db.String(100),nullable = False)
	status = db.Column(db.String(100),nullable = False)
	address = db.Column(db.String(100),nullable = False)

@app.route("/",methods=['POST','GET'])
def index():
	
	if request.method == 'POST':

		table = accounts(emails=request.form.get('email'),passwords=request.form.get('password'))
		db.session.add(table)
		db.session.commit()
		redirect('/login')
		
	return render_template('index123.html')


@app.route("/admin",methods=['POST','GET'])
def logasadmin():
	if request.method == 'POST':

		cliem = request.form.get('admin_email')
		clipass = request.form.get('admin_password')

		tab = admin_accounts.query.filter_by(emails=cliem).first()

		if tab and tab.passwords == clipass:
				session["admin_email"]=cliem


			
					
				
				return redirect('/admin_panel')
		
		else:
				return render_template('logasadmin.html',error = "Invailed Entry!!!")
			

	return render_template('logasadmin.html')

@app.route("/admin_panel",methods=['POST','GET'])
def admin_panel():
	if session.get("admin_email",None):
		
		if request.method == 'POST':
		 	
			addd = products(product_name=request.form.get('productname'),product_price=int(request.form.get('productprice')),product_description=request.form.get('productdiscription'))
			db.session.add(addd)
			db.session.commit()
			return render_template("admin_panel.html",code="product added successfully")


		order = orders.query.all()
		
		return render_template("admin_panel.html",order=order)
	else:
		return "not login"

@app.route("/admin_logout",methods=['POST','GET'])
def admin_logout():
	session.pop('admin_email',None)
	return redirect('/')

@app.route("/login",methods=['POST','GET'])
def log():

	if request.method == 'POST':
	
		cliem = request.form.get('email')
		clipass = request.form.get('password')

		tab = accounts.query.filter_by(emails=cliem).first()

		if tab and tab.passwords == clipass:
			session["email"]=cliem
			return redirect('/welcome')
			
			

			
		else:
			return render_template('login.html',error = "Invailed Entry!!!")
			


	return render_template('login.html')


@app.route("/logout",methods=['POST','GET'])
def logout():
	session.pop('email',None)
	return redirect('/')


@app.route("/welcome",methods=['POST','GET'])
def loged():
	mail = session.get("email",None)

	product = products.query.all()
	return render_template('welcome.html',email = mail,product=product)

@app.route("/orders",methods=['POST','GET'])
def order():
	mail = session.get("email",None)
	order = orders.query.filter_by(order_by=mail).all()
	return render_template('orderpage.html',order=order)

@app.route("/ordered",methods=['POST','GET'])
def ordered():
	snos = request.args.get('sno')
	
	product = products.query.filter_by(sno=snos).first()

	ore = orders(product_id=product.sno,order_by=session.get("email",None),time=datetime.now(),status="order placed",address="hdh")
	db.session.add(ore)
	db.session.commit()
	return "<p>ordered successful<p/>"

@app.route("/cart",methods=['POST','GET'])
def cart():
	its=cartitems.query.filter_by(added_by=session.get("email",None)).all()

	return render_template('cart.html',its=its)



@app.route("/addcart",methods=['POST','GET'])
def addcart():
	proid = request.args.get('sno')
	co = cartitems(added_by=session.get("email",None),product_id=proid)
	db.session.add(co)
	db.session.commit()

	return "cart added successfully"



if __name__ == "__main__":
	app.run()
