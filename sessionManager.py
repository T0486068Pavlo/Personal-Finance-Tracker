from user import User


class SessionManager:


    def __init__(self, database_manager, finance_manager, menu):
        self.database_manager = database_manager
        self.finance_manager = finance_manager
        self.menu = menu


    def validate_integer_input(self, text, min_choice, max_choice):
        choice = ''
        running = True
        while running:
            try:
                choice = int(input(text))
                if  choice < min_choice or choice > max_choice:
                    print(f"Please enter a number in range of {min_choice}-{max_choice}! ")
                    continue
                else:
                    running = False
            except ValueError:
                print("Invalid input. Try again")

        return choice

    def validate_string_input(self, text):
        choice = ''

        running = True
        while running:
            choice = input(text).strip()
            if choice == '':
                print("Cannot be empty!")
                continue
            else:
                running = False

        return choice

    def open_user_session(self, user):
        self.finance_manager.start_session(user)

        self.menu.run()

        self.finance_manager.end_session()




    def start(self):

        running = True
        while running:
            print("="*45)
            print("PERSONAL FINANCE TRACKER")
            print("="*45)

            print("1. Login")
            print("2. Create account")
            print("3. Exit")

            choice = self.validate_integer_input("Enter the number from the menu: ", 1, 3)

            match choice:
                case 1:
                    username = self.validate_string_input("Enter username: ")
                    password = self.validate_string_input("Enter your password: ")

                    row = self.database_manager.check_login(username, password)

                    if row is  None:
                        print("Incorrect password or username")
                    else:
                        user_id = row["user_id"]
                        username = row["username"]
                        currency = row["currency"]
                        password = row["password"]

                        user = User(user_id, username, currency, password)


                        self.open_user_session(user)


                case 2:
                    username = self.validate_string_input("Enter username: ")
                    currency = self.validate_string_input("Enter preferable currency: ")
                    password = self.validate_string_input("Enter your password: ")

                    user_id = self.database_manager.insert_user(username, currency, password)

                    user = User(user_id, username, currency, password)

                    self.open_user_session(user)



                case 3:
                    self.finance_manager.close_database()
                    running = False

                case _:
                    print("Invalid input")


