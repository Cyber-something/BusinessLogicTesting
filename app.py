import string, random
from flask import Flask
from flask import render_template, redirect, url_for, request, session, g
from flask_sqlalchemy import SQLAlchemy

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
    usr = User.query.filter_by(username=u).filter_by(password=p).first()
    if usr:
        sess = sess_gen()
        usr.sess = sess
        session['user'] = sess
        db.session.commit()
        if usr.is_admin:
            return redirect(url_for('admin_users'))
        else:
            return redirect(url_for('index'))

@app.get('/logout')
def logout():
    session.pop('user',None)
    g.user.sess = None
    db.session.commit()
    return redirect(url_for('login'))

@app.get('/cart')
def cart():
    u = User.query.filter_by(id=g.user.id).first()
    crypto = Crypto.query.filter_by(id=u.crypto_id).first()
    return render_template('cart.html', crypto=crypto, user=u)

@app.get('/add_cart/<id>')
def add_to_cart(id):
    u = User.query.filter_by(id=g.user.id).first()
    c = Crypto.query.filter_by(id=id).first()
    if u and c:
        u.crypto_id = c.id
        u.price = c.price
        u.quantity = 1
        u.discount = 0
        db.session.commit()
    return redirect(url_for('cart'))

@app.post('/cart/update')
def update_cart():
    qty = request.form['quantity']
    u = User.query.filter_by(id=g.user.id).first()
    if u and qty:
        u.quantity = qty
        db.session.commit()
    return redirect(url_for('cart'))

@app.post('/cart/clear')
def clear_cart():
    u = User.query.filter_by(id=g.user.id).first()
    if u:
        u.crypto_id = None
        u.quantity = 0
        u.price = 0
        u.discount = 0
        u.voucher_code = None
        db.session.commit()
    return redirect(url_for('index'))

@app.post('/cart/process')
def process_cart():
    u = User.query.filter_by(id=g.user.id).first()
    try:
        u.crypto_id = int(request.form['crypto_id'])
        u.price = int(request.form['price'])
        u.quantity = int(request.form['quantity'])
        db.session.commit()
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
            print("[+] Voucher found")
            u = User.query.filter_by(id=g.user.id).first()
            u.price = u.price - (u.price * v.percentage / 100)
            u.discount = v.percentage
            u.voucher_code = v.code
            db.session.commit()
        else:
            print("[-] Invalid voucher")
    else:
        print("[-] No code provided")
    return redirect(url_for('cart'))


@app.get('/confirm')
def confirm():
    u = User.query.filter_by(id=g.user.id).first()
    #print("Referrer: {}".format(request.referrer))
    # TODO: give the user 10 credit as loyalty for purchases
    return render_template('confirm.html', user=u)

@app.post('/checkout')
def checkout():
    # check if user has enough credit to actually buy the coins
    u = User.query.filter_by(id=g.user.id).first()
    total = u.price * u.quantity
    if total > u.credit:
        msg = "Not enough funds"
        return render_template('fail.html', msg=msg)
    else:
        # TODO: create a new order with the details
        # TODO: subtract the amount from the users credit
        o = Order(user_id=u.id, crypto_id=u.crypto_id, quantity=u.quantity, price=u.price)
        db.session.add(o)
        u.credit = u.credit - (u.price * u.quantity)
        u.crypto_id = None
        u.quantity = 0
        u.price = 0
        u.discount = 0
        u.voucher_code = None
        db.session.commit()
        return render_template('success.html')

# -----------------------------------------------------------
#   Account
# -----------------------------------------------------------

@app.get('/account')
def account():
    return render_template('account/account_details.html', opt=1)

@app.get('/account/order_history')
def order_history():
    orders = Order.query.filter_by(user_id=g.user.id).order_by(Order.id.desc()).all()
    return render_template('account/order_history.html', opt=2, orders=orders)

@app.get('/account/transfer')
def transfer_credit():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('account/transfer_credit.html', opt=3, users=users)

@app.post('/account/transfer')
def transfer_credit_user():
    user2_id = request.form['selected_user']
    amount = int(request.form['transfer_amount'])
    if user2_id and amount != 0:
        other_user = User.query.filter_by(id=user2_id).first()
        g.user.credit -= amount
        other_user.credit += amount
        db.session.commit()
    return redirect(url_for('transfer_credit'))

@app.get('/account/claim')
def claim_credit():
    return render_template('claim_credit.html', opt=4)

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

# -----------------------------------------------------------
#   Models
# -----------------------------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    sess = db.Column(db.String)
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='vouchers', lazy=True)


def sess_gen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)