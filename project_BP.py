import json
import client, admin, sample
from tables import disgner as D

db, cursor = D.get_db()

def import_from_json():
    with open('discount_codes.json', 'r') as file:
        discount_data = json.load(file)    
    for code, details in discount_data.items():
        expiry_date = details['expiry_date']
        discount = details['discount_percentage'] 
        cursor.execute('''
                INSERT OR REPLACE INTO codes (used, code, discount, date)
                VALUES (?, ?, ?, ?)
            ''', (1, str(code[4:]), int(discount), expiry_date))
        db.commit()  
        
def is_inserted():
    cursor.execute("SELECT * FROM codes ")
    movaghat = cursor.fetchall()    
    if movaghat != []:
       return True
    else :
       return False    
   
def first():
    if not is_inserted():
        sample.insert()
        import_from_json()

    while True:
        try:
            D.greeting()
            order = D.safe_input("what is your role ?\n1- client\n2- admin")
            match order:
                case "1": client.client_start() 
                case "2": admin.singin()  
        except:
            break
        
first()
db.close()
