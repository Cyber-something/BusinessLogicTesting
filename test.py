from app import db
from app import User, Crypto, Order, Voucher

def init_app():
    # Add test users
    u1 = User(username="Alice", password="ark123")
    u2 = User(username="Bob", password="ark123")
    u3 = User(username="Charlie", password="ark123")

    try:
        db.session.add_all([u1,u2,u3])
        db.session.commit()
        print("[+] Test users added")
    except Exception as e:
        print("[!] Error: User insert fail \n {}".format(e))

    # Add some test crypto
    c1 = Crypto(name="Bitcoin", price=100, icon="icon")
    c2 = Crypto(name="Ethereum", price=80, icon="icon")
    c3 = Crypto(name="Dodgecoin", price=45, icon="icon")

    try:
        db.session.add_all([c1,c2,c3])
        db.session.commit()
        print("[+] Test crypto added")
    except Exception as e:
        print("[!] Error: Crypto insert fail \n {}".format(e))

    # Add test vouchers
    v1 = Voucher(code="FREE10", percentage=10, user_id=u2.id)
    v2 = Voucher(code="SPRING15", percentage=15,user_id=u1.id)
    v3 = Voucher(code="SALE25", percentage=20)

    try:
        db.session.add_all([v1, v2, v3])
        db.session.commit()
        print("[+] Added vouchers")
    except Exception as e:
        print("[!] Error: Cannot add vouchers \n {}".format(e))

    # Add test orders
    o1 = Order(user_id=u1.id, crypto_id=c1.id, quantity=2, price=c1.price*2)
    o2 = Order(user_id=u2.id, crypto_id=c2.id, quantity=3, price=c2.price*3)
    o3 = Order(user_id=u2.id, crypto_id=c1.id, quantity=1, price=c1.price*1)
    o4 = Order(user_id=u1.id, crypto_id=c3.id, quantity=1, price=c3.price*1)
    o5 = Order(user_id=u3.id, crypto_id=c2.id, quantity=2, price=c2.price*2)

    try:
        db.session.add_all([o1,o2,o3,o4,o5])
        db.session.commit()
        print("[+] Added test orders")
    except Exception as e:
        print("[!] Error: Cannot add orders \n {}".format(e))

def recycle_db():
    try:
        db.drop_all()
        db.create_all()
    except Exception as e:
        print("[!] Error: Cannot reset database \n {}".format(e))
