import tabulate as tb
from datetime import datetime
from tables import disgner as D
from classes import client, good

db, cursor = D.get_db()

def get_time():
    return str(datetime.now().date())

def client_start():
    while True:
        try:
            D.line()
            order = D.safe_input("Choose an operation:\n1- Sing in\n2- Sing up")
            match order:
                case "1": log_in(1)
                case "2": log_in(0)
        except:
            break
        
def log_in(x:int):
    while True:
        try:
            D.line()
            data = D.safe_input("Enter your usename and password: ").split()
            check = client.sign_in(data[0], data[1], 2) if x == 1 else client.sign_up(data[0], data[1])
            if not check:
                continue
            global user
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
            order = D.safe_input('''Choose operation:\n1- new shopping\n2- history\n3- change password\n4- charge credit''')
            match order:
                case "1": new_shopping()
                case "2": history()
                case "3": change_password(user)
                case "4": charge_credit()
        except:
            break   

def show_goods():
    headers = ["ocode", "price", "num"]
    cursor.execute("SELECT * FROM goods")
    all_goods = cursor.fetchall()
    table_data = [[i[0], i[1], i[2]] for i in all_goods]
    print(tb.tabulate(table_data, headers=headers, tablefmt="simple"))
    print()
    
def new_shopping():
    while True:
        try:
            D.line()
            show_goods()
            order1 = D.safe_input("enter ocodes of good and numbers you want :")
            x = order1.split(' ')
            goods = [good(x[i]) for i in range(len(x)) if i%2==0]
            nums = [int(x[i]) for i in range(len(x)) if i%2==1]
            is_exist = True
            sum = 0
            for k in range(len(goods)):
                sum += goods[k].price * nums[k]
                if goods[k].number < nums[k]:
                    is_exist = False
            if not is_exist:
                print("This product is not available in sufficient quantity.")
                D.faild()
                continue
            elif sum > user.credit:
                print("you dont have enough credit.")
                D.faild()
                continue
            order2 = input(f"total value of shopping is :{sum}\ndo you want to buy ?\n1- yes\n2- No\n")
            if order2 == "2":
                break
            order2 = input("do you have any discount code ?\n1- yes\n2- No\n")
            discount = 0
            if order2 == "1":
                order2 = input("enter your code:")
                cursor.execute("SELECT used, date, discount FROM codes WHERE code = %r" %(order2))
                movaght = cursor.fetchone()
                if not movaght or movaght[0] == 0 or movaght[1] < get_time():
                    print("This code does not exist or has expired.")
                    D.faild()
                    continue
                discount = movaght[2]
                cursor.execute("UPDATE codes SET used = %r WHERE code = %r"%(0 , order2))
                db.commit()
            
            user.change_credit(-int(0.95*(sum - discount)))
            cursor.execute("INSERT INTO historis VALUES (%r, %r, %r, %r)" %(user.username, order1, get_time(), sum - discount))
            db.commit() 
            for l in range(len(goods)):
                goods[l].change_number(-nums[l])
            D.success(end=True)
        except:
            break
        
def history():
    cursor.execute("SELECT * FROM historis WHERE username = %r" %(user.username))
    data = cursor.fetchall()
    headers = ["name", "orders", "date", "sum"]
    print(tb.tabulate(data, headers=headers, tablefmt="simple"))
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
            order = D.safe_input("enter the amount you charge: ")
            user.change_credit(order)
            D.success(end=True)
        except:
            break


    