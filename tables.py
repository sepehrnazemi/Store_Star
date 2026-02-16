import sqlite3

class ShopDatabase:
    
    def __init__(self, db_name='shop.db'):
        self.db_name = db_name
        self.connect()
        self.create_tables()
   
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def get_db(self):
        return self.conn, self.cursor
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                access INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Extrainfos (
                username TEXT PRIMARY KEY,
                credit INTEGER,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS goods (
                ocode TEXT PRIMARY KEY,
                price INTEGER,
                number INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS codes (
                code TEXT PRIMARY KEY,
                discount INTEGER,
                date TEXT,
                used INTEGER DEFAULT 1
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS historis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                orders TEXT,
                date TEXT,
                sum INTEGER,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        ''')
        self.conn.commit()
        
    def add_user(self, username, password, access=2):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, access) VALUES (?, ?, ?)", 
                (username, password, access)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def add_extrainfo(self, username, credit=0):
        try:
            self.cursor.execute(
                "INSERT INTO Extrainfos (username, credit) VALUES (?, ?)",
                (username, credit)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_user_password(self, username, new_password):
        self.cursor.execute(
            "UPDATE users SET password = ? WHERE username = ?", (new_password, username)
        )
        self.conn.commit()
    
    def get_credit(self, username):
        self.cursor.execute(
            "SELECT credit FROM Extrainfos WHERE username = ?", (username,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    def update_credit(self, username, amount):
        self.cursor.execute(
            "UPDATE Extrainfos SET credit = credit + ? WHERE username = ?", (amount, username)
        )
        self.conn.commit()
    
    def add_product(self, ocode, price, number):
        try:
            self.cursor.execute(
                "INSERT INTO goods (ocode, price, number) VALUES (?, ?, ?)", (ocode, price, number)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_product_price(self, ocode, new_price):
        self.cursor.execute(
            "UPDATE goods SET price = ? WHERE ocode = ?", (new_price, ocode)
        )
        self.conn.commit()
    
    def update_product_stock(self, ocode, change):
        self.cursor.execute(
            "UPDATE goods SET number = number + ? WHERE ocode = ?", (change, ocode)
        )
        self.conn.commit()
    
    def get_product(self, ocode):
        self.cursor.execute(
            "SELECT price, number FROM goods WHERE ocode = ?", (ocode,)
        )
        return self.cursor.fetchone()
    
    def get_all_products(self):
        self.cursor.execute("SELECT * FROM goods")
        return self.cursor.fetchall()
    
    def add_discount_code(self, code, discount, date, used=1):
        try:
            self.cursor.execute(
                "INSERT INTO codes (code, discount, date, used) VALUES (?, ?, ?, ?)",
                (code, discount, date, used)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_discount_code(self, code):
        self.cursor.execute(
            "SELECT used, date, discount FROM codes WHERE code = ?", (code,)
        )
        return self.cursor.fetchone()
    
    def use_discount_code(self, code):
        self.cursor.execute(
            "UPDATE codes SET used = 0 WHERE code = ?", (code,)
        )
        self.conn.commit()
    
    def add_history(self, username, orders, date, total_sum):
        self.cursor.execute(
            "INSERT INTO historis (username, orders, date, sum) VALUES (?, ?, ?, ?)",
            (username, orders, date, total_sum)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_user_history(self, username):
        self.cursor.execute(
            "SELECT * FROM historis WHERE username = ? ORDER BY date DESC", (username,)
        )
        return self.cursor.fetchall()
    
    def user_exists(self, username):
        self.cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )
        return self.cursor.fetchone() is not None
    
    def verify_user(self, username, password, access_level):
        self.cursor.execute(
            "SELECT password, access FROM users WHERE username = ?", (username,)
        )
        result = self.cursor.fetchone()
        if not result or result[0] != password or result[1] != access_level:
            return False
        return True