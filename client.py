import tabulate as tb
from datetime import datetime
from designer import designer as D
from classes import client, good
from tables import ShopDatabase

db = ShopDatabase()

def get_time():
    return str(datetime.now().date())

def client_start():
    while True:
        try:
            D.line()
            order = D.safe_input("Choose an operation:\n1- Sign in\n2- Sign up")
            match order:
                case "1": 
                    log_in(1)
                case "2": 
                    log_in(0)
            break   
        except:
            break
        
def log_in(x:int):
    global user
    while True:
        try:
            D.line()
            data = D.safe_input("Enter your usename and password: ").split()
            if x == 1:
                if db.verify_user(data[0], data[1], 2):
                    user = client(data[0], data[1])
                    D.success()
                    client_menu()
                else:
                    D.failed()        
            else:
                if client.sign_up(data[0], data[1]):
                    user = client(data[0], data[1])
                    D.success()
                    client_menu()     
        except:
            break
           
def client_menu():
    while True:
        try:
            D.menu("client")
            print(f"CREDIT : {user.credit}")
            order = D.safe_input('''Choose operation:
   1- new shopping \n   2- history \n   3- change password \n   4- charge credit
    ''')
            match order:
                case "1": new_shopping()
                case "2": history()
                case "3": change_password(user)
                case "4": charge_credit()
        except:
            break   

def show_goods():
    headers = ["ocode", "price", "num"]
    all_goods = db.get_all_products()
    table_data = [[i[0], i[1], i[2]] for i in all_goods]
    print(tb.tabulate(table_data, headers=headers, tablefmt="simple"))
    print()
    
def new_shopping():
    while True:
        try:
            D.line()
            show_goods()
            order1 = D.safe_input("Enter product codes and quantities :")
            x = order1.split(' ')
            if len(x) % 2 != 0:
                continue
            goods = [good(x[i]) for i in range(len(x)) if i%2==0]
            nums = [int(x[i]) for i in range(len(x)) if i%2==1]
            is_exist = True
            total = 0
            for k in range(len(goods)):
                total += goods[k].price * nums[k]
                if goods[k].number < nums[k]:
                    is_exist = False
                    print(f"{goods[k].ocode} not enough stock available")
            if not is_exist:
                D.failed()
                continue
            elif total > user.credit:
                print("You dont have enough credit.")
                D.failed()
                continue
            order2 = input(f"Total value of shopping is :{total}\nDo you wish to proceed? ?\n1- Yes\n2- No\n")
            if order2 == "2":
                break
            order2 = input("Do you have a discount code ?\n1- Yes\n2- No\n")
            discount = 0
            if order2 == "1":
                code = input("Enter your code:")
                code_info = db.get_discount_code(code)
                if not code_info or code_info[0] == 0 or code_info[1] < get_time():
                    print("Invaid or expired discount code")
                    D.failed()
                    continue
                discount = code_info[2]
                db.use_discount_code(code)
            
            user.change_credit(-int(0.95*(total - discount)))
            db.add_history(user.username, order1, get_time(), total - discount)
            for l in range(len(goods)):
                goods[l].change_number(-nums[l])
            D.success(end=True)
        except:
            break
        
def history():
    data = db.get_user_history(user.username)
    headers = ["name", "orders", "date", "sum"]
    display_data = [[d[1], d[2], d[3], d[4]] for d in data]
    print(tb.tabulate(display_data, headers=headers, tablefmt="simple"))
    print()
    
def change_password(x:client):
    while True:
        try:
            D.line()
            order = D.safe_input("Enter your new password:")
            if not x.change_password(order):
                continue 
            D.success(end=True)
        except:
            break   
 
def charge_credit():
    while True:
        try:
            D.line()
            order = D.safe_input("Enter the amount you wish to charge: ")
            user.change_credit(int(order))
            D.success(end=True)
        except:
            break