import json
from tables import ShopDatabase

db = ShopDatabase()

def import_from_json():
    with open('discount_codes.json', 'r') as file:
        discount_data = json.load(file)   

    for code, details in discount_data.items():
        code_num = code[4:]
        expiry_date = details['expiry_date']
        discount = details['discount_percentage']
        db.add_discount_code(code_num, discount, expiry_date)
        
def authors_account():
    authors = [('Sepehr', 'sepehr1385', 1), ('Shayan', 'shayan1386', 1), 
               ('Noorin', 'noorin1385', 1), ('Parand', 'parand1385', 1)]
    for username, password, access in authors:
        db.add_user(username, password, access)   

def sample():
    users = [('admin', 'admin123', 1), ('ali', 'Ali12345', 2),
             ('sara', 'Sara12345', 2)]
    for username, password, access in users:
        db.add_user(username, password, access)
    db.add_extrainfo('ali', 500000)
    db.add_extrainfo('sara', 300000)
    
    products = [
    ('Laptop Asus', 35000000, 10),
    ('Logitech Mouse', 500000, 50),
    ('Mechanical Keyboard', 2000000, 20),
    ('Sony Headphone', 1500000, 15)] 
    
    for ocode, price, number in products:
        db.add_product(ocode, price, number)
    
