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
            print("3. Edit transaction")
            print("4. View all transactions")
            print("5. Filter transactions")
            print("6. Search transaction")
            print("7. Manage categories")
            print("8. View statistics ")
            print("9. Exit")


            choice = int(input("Enter your choice: "))


            match choice:

                case 1:
                    self.finance_manager.add_transaction()
                case 2:
                    pass

                case 4:
                    self.finance_manager.list_transactions()

                case 9:
                    print("Goodbye")
                    running = False




    def run(self):
        self.display_menu()