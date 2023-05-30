import json
from flask import Flask,render_template,request,jsonify,redirect,url_for,make_response,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import razorpay

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'PAYMENT_APP'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payment.db'
app.config['SQLALCHEMY_BINDS'] = {'qna':'sqlite:///qna.db'}

# Booking Database
class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(120),nullable = False)
    name = db.Column(db.String(120),nullable = False)
    amount = db.Column(db.String(120),nullable = False)
# Booking Database Complete 

# Review Database 
class QnA(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    desc = db.Column(db.String(500),nullable = False)
    title =db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime,default = datetime.now().replace(microsecond=0))
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Review Database Created

@app.route('/')
def Home():
    return render_template('index.html')
    
    # Booking


@app.route('/templates/bookings.html',methods = ['GET','POST'])
def hello():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        amount = request.form.get('amount')
        user =Users(email = email,name = name,amount = amount)
        db.session.add(user)
        db.session.commit()
        print(user)
        return redirect(url_for('pay',id = user.id))

    return render_template('bookings.html')

@app.route('/pay/<id>',methods = ['GET','POST'])
def pay(id):
    user = Users.query.filter_by(id = id).first()
    client = razorpay.Client(auth = ("rzp_live_USjrZ32YOBOYUb","lN0TFCGYDeDOeeOwSREd20b4"))
    payment = client.order.create({'amount':int(user.amount)*100,'currency':'INR','payment_capture':'1'})
    return render_template('pay.html',payment = payment)

@app.route('/success',methods = ['GET','POST'])
def success():
    return render_template('success.html')


    # Booking Done 


    # Review Route 
@app.route('/templates/review.html', methods = ['GET', 'POST'])
def heloqna():
    if request.method == 'POST':
        
        title = request.form['title']
        desc = request.form['desc']
        qna = QnA(title =title,desc = desc)
        db.session.add(qna)
        db.session.commit()
        return redirect("/templates/review.html") 
        #boolean -false

    allqna = QnA.query.all()
    
    return render_template("review.html",allqna = allqna)

# Finished

@app.route('/templates/Gallery_Trending.html')
def Trending():
    return render_template('Gallery_Trending.html')

@app.route('/templates/Gallery_Bridal.html',methods = ['GET','POST'])
def Bridal():
    return render_template('Gallery_Bridal.html')

@app.route('/templates/Gallery_engagement.html',methods = ['GET','POST'])
def engagement():
    return render_template('Gallery_engagement.html')

@app.route('/templates/Gallery_reception.html',methods = ['GET','POST'])
def reception():
    return render_template('Gallery_reception.html')

@app.route('/templates/Gallery_ocasionally.html',methods = ['GET','POST'])
def ocasionally():
    return render_template('Gallery_ocasionally.html')




if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.run(debug = True,port = 8000)
    FLASK_APP = app.py