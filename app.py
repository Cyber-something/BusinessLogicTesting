from flask import Flask
from flask import render_template, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.get('/login')
def login():
    return render_template('login.html')

@app.post('/login')
def login_post():
    return redirect(url_for('index'))

@app.get('/logout')
def logout():
    return redirect(url_for('login'))

@app.get('/cart')
def cart():
    return render_template('cart.html')

@app.get('/confirm')
def confirm():
    return render_template('confirm.html')

@app.get('/account')
def account():
    return render_template('account_details.html', opt=1)

@app.get('/account/order_history')
def order_history():
    return render_template('order_history.html', opt=2)

@app.get('/account/transfer')
def transfer_credit():
    return render_template('transfer_credit.html', opt=3)

@app.get('/account/claim')
def claim_credit():
    return render_template('claim_credit.html', opt=4)

@app.get('/admin')
def admin():
    return render_template('admin.html')



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
