from tables import disgner as D
from classes import admin, good
from client import change_password

db, cursor = D.get_db()

def singin():
    while True:
        try:
            D.line()
            data = D.safe_input("Enter your usename and password: ").split()
            check = admin.sign_in(data[0], data[1], 1)
            if not check :
                D.faild()
                continue
            global user
            user = admin(data[0], data[1]) 
            D.success()
            admin_menu()   
        except:
            break
            
def admin_menu():
    while True:
        try:
            D.menu("admin")
            order = D.safe_input('''Choose operation:\n1- add good\n2- change inventory of goods\n3- change price of goods\n4- change password ''')
            match order:
                case "1": add_good()
                case "2": change_inventory()
                case "3": change_price()
                case "4": change_password(user)
        except:
            break        
            
def add_good():
    while True:
        try:
            D.line()
            order = D.safe_input("enter ocode, price, number of good : ").split(' ')
            cursor.execute("INSERT INTO goods VALUES (%r, %r, %r)" %(order[0], int(order[1]), int(order[2])))
            db.commit()
            D.success(end=True)
        except:
            break
    
def change_inventory():
    while True:
        try:
            D.line()
            order = D.safe_input("enter ocode and changed inventory:").split(' ')
            my_good = good(order[0])  
            my_good.change_number(order[1])
            D.success(end=True)
        except:
            break
    
def change_price():
    while True:
        try:
            D.line()
            order = D.safe_input("enter ocode and changed price: ").split(' ')
            my_good = good(order[0])
            my_good.change_price(order[1])
            D.success(end=True)
        except:
            break
        

