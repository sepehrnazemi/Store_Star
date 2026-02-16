class designer:   

    @staticmethod
    def safe_input(prompt):
        prompt = prompt + "\nback\nquit\n"
        user_input = input(prompt)
        if user_input == "back":
            raise Exception() 
        elif user_input == "quit":
            exit()
        return user_input

    def greeting():
        print("------------ Welcome to StarStore 🥳 -------------\n")

    def menu(x):
        x = x.title()
        if x == "Admin":
            print(f"------------------ {x} Menu 👑 -------------------\n")
        else:
            print(f"------------------ {x} Menu 💻 ------------------\n")

    def line():
        print("---------------------------------------------------\n")

    def success(end=False):
        print("----------- The Operation was successfull ✅ -----------\n")
        if end : raise Exception()

    def failed():
        print("-------------- The Operation failed ❌ --------------\n")

    def error():
        print("-------------------- ❗ Error ❗ --------------------\n")