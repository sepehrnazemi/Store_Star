from designer import designer as D
from tables import ShopDatabase

db = ShopDatabase()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
          
    def change_password(self, order):
        if not self.password_identifier(order):
            print("This password is not strong enough.")
            D.failed()
            return False
        self.password = order
        db.update_user_password(self.username, order)
        return True

    @staticmethod
    def password_identifier(password):
        errors = []
        if len(password) < 8:
            errors.append("Please use at least 8 characters with mix of letters and numbers.")
        has_upper = has_lower = has_digit = False
        for char in password:
            if 'A' <= char <= 'Z': has_upper = True
            elif 'a' <= char <= 'z': has_lower = True
            elif '0' <= char <= '9': has_digit = True
        if not has_upper: errors.append("Password must contain at least one uppercase letter")
        if not has_lower: errors.append("Password must contain at least one lowercase letter")
        if not has_digit: errors.append("Password must contain at least one digit")
        
        if errors:
            print("\n".join(errors))
            D.failed()
            return False
            
        return True    
                  
class admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
    
class client(User):
    def __init__(self, username, password):
        super().__init__(username, password)  
        self.credit = db.get_credit(username)
        
    def change_credit(self, order):
        self.credit += int(order)
        db.update_credit(self.username, int(order))
        
    @staticmethod
    def sign_up(username, password):
        if db.user_exists(username):
            print("This username already exists.")
            D.failed()
            return False
        if not client.password_identifier(password):
            print("This password is not strong enough.")
            D.failed()
            return False
        db.add_user(username, password, 2)
        db.add_extrainfo(username, 0)
        return True

class good:
    def __init__(self, ocode):
        self.ocode = ocode
        product = db.get_product(ocode)
        if product:
            self.price, self.number = product
            self.exists = True
        else:
            self.price = self.number = 0
            self.exists = False
    
    def change_number(self, order):
        self.number += order
        db.update_product_stock(self.ocode, order)
        
    def change_price(self, order):
        self.price = order
        db.update_product_price(self.ocode, order)