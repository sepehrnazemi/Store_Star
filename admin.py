from designer import designer as D
from classes import admin, good
from client import change_password
from tables import ShopDatabase

db = ShopDatabase()

def singin():
    global user
    while True:
        try:
            D.line()
            data = D.safe_input("Enter your usename and password: ").split()
            if db.verify_user(data[0], data[1], 1):
                user = admin(data[0], data[1]) 
                D.success()
                admin_menu()
            else:
                D.failed()
        except:
            break
            
def admin_menu():
    while True:
        try:
            D.menu("admin")
            order = D.safe_input('''Choose operation:
   1- add good \n   2- inventory management \n   3- price management \n   4- change password 
    ''')
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
            order = D.safe_input("Enter product details : ( Code, Price, Quantity) ").split(' ')
            if len(order) != 3:
                continue
            my_good = good(order[0])
            if my_good.exists:
                print("Product with this code already exists")
                D.failed()
            else:
                db.add_product(order[0], int(order[1]), int(order[2]))
                D.success(end=True)
        except:
            break
    
def change_inventory():
    while True:
        try:
            D.line()
            order = D.safe_input("Enter ocode and changed inventory:").split(' ')
            if len(order) != 2:
                continue
            my_good = good(order[0])
            if my_good.exists:
                my_good.change_number(int(order[1]))
                D.success(end=True)
            else:
                print("Product not found")
                D.failed()
        except:
            break
    
def change_price():
    while True:
        try:
            D.line()
            order = D.safe_input("Enter ocode and changed price: ").split(' ')
            if len(order) != 2:
                continue
            my_good = good(order[0])
            if my_good.exists:
                my_good.change_price(int(order[1]))
                D.success(end=True)
            else:
                print("Product not found")
                D.failed()
        except:
            break