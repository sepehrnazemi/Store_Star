import sqlite3

class disgner:   
      
   @staticmethod
   def safe_input(prompt):
      prompt = prompt + "\nexit- return\nexitexit- end\n"
      user_input = input(prompt)
      if user_input == "exit":
         raise Exception() 
      elif user_input == "exitexit":
         exit()
      return user_input
         
   @staticmethod
   def get_db():
     db = sqlite3.connect('sql.db')
     cursor = db.cursor()
     creat_tables(cursor)
     return db, cursor

   def greeting():
      print("_______________Welcome_to_our_website______________\n")
   def menu(x):
      print(f"___________________{x}_menu__________________\n")
   def line():
      print(f"__________________________________________________\n")
   def success(end=False):
      print("_____________operation_was_successfull_____________\n")
      if end : raise Exception()
   def faild(con=True):
      print("________________operation_was_faild________________\n")
             
def creat_tables(cursor):
    cursor.execute('''
          CREATE TABLE IF NOT EXISTS users
          ([username] TEXT, [password] TEXT, [access] INTEGER)
          ''')
    cursor.execute('''
          CREATE TABLE IF NOT EXISTS Extrainfos
          ([username] TEXT, [credit] INTEGER)
          ''')
    cursor.execute('''
          CREATE TABLE IF NOT EXISTS goods
          ([ocode] TEXT, [price] INTEGER, [number] INTEGER)
          ''')
    cursor.execute('''
          CREATE TABLE IF NOT EXISTS codes
          ([used] INTEGER, [code] INTEGER, [discount] INTEGER, [date] TEXT)
          ''')
    cursor.execute('''
          CREATE TABLE IF NOT EXISTS historis
          ([username] TEXT, [orders] TEXT,[date] TEXT,[sum] INTEGER)
          ''')
    
