from tables import disgner as D

db, cursor = D.get_db()

def insert_admin(username,password):
    cursor.execute("INSERT INTO users VALUES (%r, %r, %r)" %(username, password, 1))
    db.commit()
    
def insert_client(username,password):
    cursor.execute("INSERT INTO Extrainfos VALUES (%r, %r)" %(username, 0))
    cursor.execute("INSERT INTO users VALUES (%r, %r, %r)" %(username, password, 2))
    db.commit()    
    
def insert_good(ocode,price,number):
    cursor.execute("INSERT INTO goods VALUES (%r, %r, %r)" %(ocode, price, number))
    db.commit()
    
def insert():
    insert_good("o_orange", 12, 5)
    insert_good("o_apple", 5, 8)
    insert_good("o_carrot", 7, 10)
    insert_good("o_watermelon", 12, 5)
    insert_client("sepehr", "Sepehr1385")
    insert_client("parand", "Parand1385")
    insert_admin("shayan", "Shayan1385")
    insert_admin("norin", "Norin1385")
    
