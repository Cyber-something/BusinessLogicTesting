from app import db
from app import User, Crypto, Order, Voucher
from app import sess_gen
from werkzeug.security import generate_password_hash, check_password_hash

def init_app():

    p1 = generate_password_hash("password")
    p2 = generate_password_hash("admin")

    # Add test users
    u1 = User(username="admin", password=p2, is_admin=True)
    u2 = User(username="alice", password=p1, credit=1450)
    u3 = User(username="bob", password=p1, credit=1300)
    u4 = User(username="charlie", password=p1, credit=1560)
    u5 = User(username="student", password=p1, credit=2000)
    

    try:
        db.session.add_all([u1,u2,u3,u4,u5])
        db.session.commit()
        print("[+] Test users added")
    except Exception as e:
        print("[!] Error: User insert fail \n {}".format(e))

    # Add some test crypto
    c1 = Crypto(name="Bitcoin", price=100, icon='<svg xmlns="http://www.w3.org/2000/svg" width="5rem" height="5rem" fill="currentColor" class="bi bi-currency-bitcoin" viewBox="0 0 16 16"> <path d="M5.5 13v1.25c0 .138.112.25.25.25h1a.25.25 0 0 0 .25-.25V13h.5v1.25c0 .138.112.25.25.25h1a.25.25 0 0 0 .25-.25V13h.084c1.992 0 3.416-1.033 3.416-2.82 0-1.502-1.007-2.323-2.186-2.44v-.088c.97-.242 1.683-.974 1.683-2.19C11.997 3.93 10.847 3 9.092 3H9V1.75a.25.25 0 0 0-.25-.25h-1a.25.25 0 0 0-.25.25V3h-.573V1.75a.25.25 0 0 0-.25-.25H5.75a.25.25 0 0 0-.25.25V3l-1.998.011a.25.25 0 0 0-.25.25v.989c0 .137.11.25.248.25l.755-.005a.75.75 0 0 1 .745.75v5.505a.75.75 0 0 1-.75.75l-.748.011a.25.25 0 0 0-.25.25v1c0 .138.112.25.25.25L5.5 13zm1.427-8.513h1.719c.906 0 1.438.498 1.438 1.312 0 .871-.575 1.362-1.877 1.362h-1.28V4.487zm0 4.051h1.84c1.137 0 1.756.58 1.756 1.524 0 .953-.626 1.45-2.158 1.45H6.927V8.539z" /> </svg>')
    c2 = Crypto(name="Ethereum", price=80, icon='<svg xmlns="http://www.w3.org/2000/svg" width="5rem" height="5rem" fill="currentColor" class="bi bi-x-diamond" viewBox="0 0 16 16"><path d="M7.987 16a1.526 1.526 0 0 1-1.07-.448L.45 9.082a1.531 1.531 0 0 1 0-2.165L6.917.45a1.531 1.531 0 0 1 2.166 0l6.469 6.468A1.526 1.526 0 0 1 16 8.013a1.526 1.526 0 0 1-.448 1.07l-6.47 6.469A1.526 1.526 0 0 1 7.988 16zM7.639 1.17 4.766 4.044 8 7.278l3.234-3.234L8.361 1.17a.51.51 0 0 0-.722 0zM8.722 8l3.234 3.234 2.873-2.873c.2-.2.2-.523 0-.722l-2.873-2.873L8.722 8zM8 8.722l-3.234 3.234 2.873 2.873c.2.2.523.2.722 0l2.873-2.873L8 8.722zM7.278 8 4.044 4.766 1.17 7.639a.511.511 0 0 0 0 .722l2.874 2.873L7.278 8z" /></svg>')
    c3 = Crypto(name="Dodgecoin", price=45, icon='<svg xmlns="http://www.w3.org/2000/svg" width="5rem" height="5rem" fill="currentColor" class="bi bi-coin" viewBox="0 0 16 16"><path d="M5.5 9.511c.076.954.83 1.697 2.182 1.785V12h.6v-.709c1.4-.098 2.218-.846 2.218-1.932 0-.987-.626-1.496-1.745-1.76l-.473-.112V5.57c.6.068.982.396 1.074.85h1.052c-.076-.919-.864-1.638-2.126-1.716V4h-.6v.719c-1.195.117-2.01.836-2.01 1.853 0 .9.606 1.472 1.613 1.707l.397.098v2.034c-.615-.093-1.022-.43-1.114-.9H5.5zm2.177-2.166c-.59-.137-.91-.416-.91-.836 0-.47.345-.822.915-.925v1.76h-.005zm.692 1.193c.717.166 1.048.435 1.048.91 0 .542-.412.914-1.135.982V8.518l.087.02z" /><path fill-rule="evenodd" d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" /><path fill-rule="evenodd" d="M8 13.5a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zm0 .5A6 6 0 1 0 8 2a6 6 0 0 0 0 12z" /></svg>')

    try:
        db.session.add_all([c1,c2,c3])
        db.session.commit()
        print("[+] Test crypto added")
    except Exception as e:
        print("[!] Error: Crypto insert fail \n {}".format(e))

    # Add test vouchers
    v1 = Voucher(code="FREE10", percentage=10)
    v2 = Voucher(code="SPRING15", percentage=15)
    v3 = Voucher(code="SALE25", percentage=25)
    v4 = Voucher(code="SALE15", percentage=15)
    v5 = Voucher(code="PS35", percentage=35)

    try:
        db.session.add_all([v1, v2, v3, v4, v5])
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


if __name__ == "__main__":
    recycle_db()
    init_app()