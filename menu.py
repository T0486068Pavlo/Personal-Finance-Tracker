from financeManager import FinanceManager
class Menu:


    def __init__(self, finance_manager):
        self.finance_manager = finance_manager



    def display_menu(self):
        running = True
        while running:

            print("PERSONAL FINANCE TRACKER")
            print("1. Add transaction")
            print("2. Delete transaction")
            print("3. Manage categories")
            print("4. Edit transaction")
            print("5. View all transactions")
            print("6. Filter transactions")
            print("7. Search transaction")
            print("8. View statistics ")
            print("9. Exit")


            choice = int(input("Enter your choice: "))


            match choice:

                case 1:
                    self.finance_manager.add_transaction()

                case 5:
                    self.finance_manager.show_transaction()

                case 9:
                    print("Goodbye")
                    running = False




    def run(self):
        self.display_menu()