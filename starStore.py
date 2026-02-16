import client, admin, generated_data
from designer import designer as D
from tables import ShopDatabase

db = ShopDatabase()

def is_inserted():
    return db.get_all_products() != []

def start():
    if not is_inserted():
        generated_data.import_from_json()
        generated_data.authors_account()
        generated_data.sample()

    while True:
        try:
            D.greeting()
            order = D.safe_input("select your role:\n1- client\n2- admin")
            match order:
                case "1":client.client_start()         
                case "2":admin.singin()
                case _:
                    D.error()
                    print("Invalid command. Please try again.\n")
        except:
            break
        
start()
db.close()