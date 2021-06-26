import string, random
from flask import Flask
from flask import render_template, redirect, url_for, request, session, g, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "what3v3r"
db = SQLAlchemy(app)


@app.route('/')
def index():
    c = Crypto.query.all()
    return render_template('index.html',crypto=c)

@app.before_request
def before_req():
    if request.endpoint not in ['login','login_post','static']:
        if 'user' not in session: #or 'user' not in g
            return redirect(url_for('login'))
        else:
            # validate the session
            usr = User.query.filter_by(sess=session['user']).first()
            if usr:
                g.user = usr
            else:
                print("[!] Invalid session")
                session.pop('user',None)
                return redirect(url_for('login'))

@app.get('/login')
def login():
    if "user" in g:
        print("[!] {}".format(g.user))
    return render_template('login.html')

@app.post('/login')
def login_post():
    u = request.form['username']
    p = request.form['password']
    usr = User.query.filter_by(username=u).first()
    if usr:
        if check_password_hash(usr.password,p):
            sess = sess_gen()
            usr.sess = sess
            session['user'] = sess
            db.session.commit()
            if usr.is_admin:
                return redirect(url_for('admin_users'))
            else:
                return redirect(url_for('index'))
        else:
            print("[!] Wrong password")
            
    else:
        print("[!] Wrong username")
    flash("Wrong username or password", "danger")
    return redirect(url_for('login'))

@app.get('/logout')
def logout():
    session.pop('user',None)
    g.user.sess = None
    db.session.commit()
    return redirect(url_for('login'))

@app.get('/cart')
def cart():
    c = Crypto.query.filter_by(id=g.user.crypto_id).first()
    if g.user.crypto_id: 
        return render_template('cart.html', crypto=c)
    else:
        return redirect(url_for('index'))

@app.get('/add_cart/<id>')
def add_to_cart(id):
    c = Crypto.query.filter_by(id=id).first()
    if c:
        g.user.crypto_id = c.id
        g.user.price = c.price
        g.user.quantity = 1
        g.user.discount = 0
        db.session.commit()
    return redirect(url_for('cart'))

@app.post('/cart/update')
def update_cart():
    qty = request.form['quantity']
    if qty:
        g.user.quantity = qty
        db.session.commit()
    return redirect(url_for('cart'))

@app.post('/cart/clear')
def clear_cart():
    if g.user.crypto_id:
        g.user.crypto_id = None
        g.user.quantity = 0
        g.user.price = 0
        g.user.discount = 0
        g.user.voucher_code = None
        db.session.commit()
    return redirect(url_for('index'))

@app.post('/cart/process')
def process_cart():
    try:
        g.user.crypto_id = int(request.form['crypto_id'])
        g.user.price = int(request.form['price'])
        g.user.quantity = int(request.form['quantity'])
        g.user.credit += 10
        db.session.commit()
        flash("10 Credits awarded for your order ", "info")
    except Exception as e:
        print("There was an error: {}".format(e))
    return redirect(url_for('confirm'))


@app.post('/claim_voucher')
def claim_voucher():
    # get the user id
    c = request.form['code']
    if c:
        v = Voucher.query.filter_by(code=c.upper()).filter_by(user_id=None).first()
        if v:
            g.user.price = (int)(g.user.price - (g.user.price * v.percentage / 100))
            g.user.discount = v.percentage
            g.user.voucher_code = v.code
            v.user_id = g.user.id
            db.session.commit()
        else:
            flash("Invalid Voucher", "warning")
    else:
        flash("No voucher code provided", "warning")
    return redirect(url_for('cart'))


@app.get('/confirm')
def confirm():
    u = User.query.filter_by(id=g.user.id).first()
    c = Crypto.query.filter_by(id=u.crypto_id).first()
    total = (int)(u.price * u.quantity * (100 - u.discount) / 100)
    if u.reg_bonus:
        total = (int)(u.price*0.9)
    #print("Referrer: {}".format(request.referrer))
    # TODO: give the user 10 credit as loyalty for purchases
    return render_template('confirm.html', user=u, t=total, crypto=c)

@app.get('/checkout')
def checkout():
    # check if user has enough credit to actually buy the coins
    total = g.user.price * g.user.quantity
    if total > g.user.credit:
        msg = "Not enough funds"
        return render_template('fail.html', msg=msg)
    else:
        if g.user.reg_bonus:
            g.user.price = (int)(g.user.price * 0.9)
        o = Order(user_id=g.user.id, crypto_id=g.user.crypto_id, quantity=g.user.quantity, price=g.user.price)
        db.session.add(o)
        g.user.credit = g.user.credit - (g.user.price * g.user.quantity)
        g.user.crypto_id = None
        g.user.quantity = 0
        g.user.price = 0
        g.user.discount = 0
        g.user.voucher_code = None
        g.user.reg_bonus = False
        db.session.commit()
        return render_template('success.html')

# -----------------------------------------------------------
#   Account
# -----------------------------------------------------------

@app.get('/account')
def account():
    o = Order.query.filter_by(user_id=g.user.id).all()
    c = Crypto.query.all()
    dt = []
    for i in c:
        sum = 0
        for j in o:
            if i.id == j.crypto_id:
                sum += j.quantity
        dt.append({"crypto":i.name, "amount":sum})
    return render_template('account/account_details.html', opt=1, o=o, dt=dt)

@app.get('/account/order_history')
def order_history():
    orders = Order.query.filter_by(user_id=g.user.id).order_by(Order.id.desc()).all()
    return render_template('account/order_history.html', opt=2, orders=orders)

@app.get('/account/transfer')
def transfer_credit():
    users = User.query.filter_by(is_admin=False).filter(User.id!=g.user.id).all()
    return render_template('account/transfer_credit.html', opt=3, users=users)

@app.post('/account/transfer')
def transfer_credit_user():
    user2_id = request.form['selected_user']
    amount = int(request.form['transfer_amount'])
    if user2_id and amount != 0:
        print("trnasfer {} from {} to user {}".format(amount,g.user.id,user2_id))
        other_user = User.query.filter_by(id=user2_id).first()
        g.user.credit -= amount
        other_user.credit += amount
        db.session.commit()

    return redirect(url_for('transfer_credit'))

"""
@app.get('/account/claim')
def claim_credit():
    return render_template('claim_credit.html', opt=4)
"""

# -----------------------------------------------------------
#   Admin
# -----------------------------------------------------------

@app.get('/admin')
def admin():
    return redirect(url_for("admin_users"))

@app.get('/admin/users')
def admin_users():
    users = User.query.all()
    return render_template('admin/admin_users.html', opt=1, users=users)

@app.get('/admin/users/add_credit/<id>')
def admin_add_credit(id):
    u = User.query.filter_by(id=id).first()
    if u:
        u.credit += 50
        db.session.commit()
    return redirect(url_for('admin_users'))

@app.get('/admin/crypto')
def admin_crypto():
    crypto = Crypto.query.all()
    return render_template('admin/admin_crypto.html', opt=2, crypto=crypto)

@app.get('/admin/crypto/inc/<id>')
def inc_crypto_price(id):
    c = Crypto.query.filter_by(id=id).first()
    if c:
        c.price += 5
        db.session.commit()
    return redirect(url_for('admin_crypto'))

@app.get('/admin/crypto/dec/<id>')
def dec_crypto_price(id):
    c = Crypto.query.filter_by(id=id).first()
    if c:
        c.price -= 5
        db.session.commit()
    return redirect(url_for('admin_crypto'))

@app.get('/admin/orders')
def admin_orders():
    # User.query.order_by(User.id.desc()).all()
    orders = Order.query.order_by(Order.id.desc()).all()
    return render_template('admin/admin_orders.html', opt=3, orders=orders)

@app.get('/admin/vouchers')
def admin_vouchers():
    vouchers = Voucher.query.all()
    return render_template('admin/admin_vouchers.html', opt=4, vouchers=vouchers)

@app.get('/admin/vouchers/reset/<id>')
def reset_voucher(id):
    v = Voucher.query.filter_by(id=id).first()
    if v:
        v.user_id = None
        db.session.commit()
    return redirect(url_for('admin_vouchers'))

# -----------------------------------------------------------
#   Models
# -----------------------------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    sess = db.Column(db.String)
    reg_bonus = db.Column(db.Boolean, nullable=False, default=True)
    credit = db.Column(db.Integer, default=100)
    crypto_id = db.Column(db.Integer, db.ForeignKey('crypto.id'), default=None)
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)
    discount = db.Column(db.Integer, default=0)
    voucher_code = db.Column(db.String, default=None)
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)
    user = db.relationship('User', backref='vouchers', lazy=True)


def sess_gen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)