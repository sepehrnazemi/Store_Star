from tables import disgner as D

db, cursor = D.get_db()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
          
    def change_password(self, order):
        check = True
        if not self.password_identifier(order):
            print("This password is not strong enough.")
            check = False
            D.faild()
        self.password = order
        cursor.execute("UPDATE users SET password = %r WHERE username = %r" %(order, self.username))
        db.commit()
        return check

    @staticmethod
    def sign_in(useruame, password, x):
        cursor.execute("SELECT password, access FROM users WHERE username = %r" %(useruame))
        movaghat = cursor.fetchone()
        check = True
        if not movaghat or movaghat[0] != password:
            print("Incorrect username or password!")
            check = False
        access = movaghat[1]
        if access != x :
            print("you dont have access.")
            check = False
        return check

    @staticmethod
    def password_identifier(password):
        if len(password) < 8:
            return False
        has_upper = False
        has_lower = False
        has_digit = False
    
        for char in password:
            if 'A' <= char <= 'Z':
                has_upper = True
            elif 'a' <= char <= 'z':
                has_lower = True
            elif '0' <= char <= '9':
                has_digit = True
                
        return has_upper and has_lower and has_digit
    
class admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
    
class client(User):
    def __init__(self, username, password):
        super().__init__(username, password)  
        cursor.execute("SELECT credit FROM Extrainfos WHERE username = %r" %(self.username))
        result = cursor.fetchone()
        self.credit = int(result[0]) if result else 0 
        
    def change_credit(self, order):
        self.credit += int(order)
        cursor.execute("UPDATE Extrainfos SET credit = %r WHERE username = %r"%(self.credit, self.username))
        db.commit()    
        
    @staticmethod
    def sign_up(useruame, password):
        cursor.execute("SELECT * FROM users WHERE username = %r" %(useruame))
        movaghat = cursor.fetchall()
        check = True
        if movaghat != [] : 
            print("this username has already exist.")
            D.faild()
            check = False
        elif not client.password_identifier(password):
            print("This password is not strong enough.")
            D.faild()
            check = False
        cursor.execute("INSERT INTO users VALUES (%r, %r, %r)" %(useruame, password, 2))
        cursor.execute("INSERT INTO Extrainfos VALUES (%r, %r)" %(useruame, 0))
        db.commit()
        return check

class good:
    def __init__(self, ocode):
        self.ocode = ocode
        cursor.execute("SELECT price, number FROM goods WHERE ocode = %r" %(self.ocode))
        movaghat = cursor.fetchone()
        self.price = movaghat[0]
        self.number = movaghat[1]
    
    def change_number(self, order):
        self.number += order
        cursor.execute("UPDATE goods SET number = %r WHERE ocode = %r"%(self.number, self.ocode))
        db.commit()
        
    def change_price(self, order):
        self.price = order
        cursor.execute("UPDATE goods SET price = %r WHERE ocode = %r"%(self.price, self.ocode))
        db.commit()