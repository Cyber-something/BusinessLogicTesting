from flask import Flask
from flask import render_template, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    return redirect(url_for("admin_users"))

@app.get('/admin/users')
def admin_users():
    users = User.query.all()
    return render_template('admin/admin_users.html', opt=1, users=users)

@app.get('/admin/crypto')
def admin_crypto():
    crypto = Crypto.query.all()
    return render_template('admin/admin_crypto.html', opt=2, crypto=crypto)

@app.get('/admin/orders')
def admin_orders():
    orders = Order.query.all()
    return render_template('admin/admin_orders.html', opt=3, orders=orders)

@app.get('/admin/vouchers')
def admin_vouchers():
    vouchers = Voucher.query.all()
    return render_template('admin/admin_vouchers.html', opt=4, vouchers=vouchers)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    sess = db.Column(db.String)
    credit = db.Column(db.Integer, default=100)
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)

    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Crypto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    icon = db.Column(db.Text, nullable=False)

    orders = db.relationship('Order', backref='crypto', lazy=True)

    def __repr__(self):
        return '<Crypto %r>' % self.name


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)
    crypto_id = db.Column(db.Integer, db.ForeignKey('crypto.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Voucher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    percentage = db.Column(db.Integer, nullable=False, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref='vouchers', lazy=True)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)