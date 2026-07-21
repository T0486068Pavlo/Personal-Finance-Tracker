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
            print("5. Search transaction")
            print("6. Manage categories")
            print("7. View statistics ")
            print("8. Exit")


            choice = int(input("Enter your choice: "))


            match choice:

                case 1:
                    self.finance_manager.add_transaction()
                case 2:
                    self.finance_manager.delete_transaction()
                case 3:
                    self.finance_manager.edit_transaction()
                case 4:
                    self.finance_manager.list_transactions()
                case 5:
                    self.finance_manager.search_transaction()
                case 6:
                    self.finance_manager.manage_categories()
                case 7:
                    self.finance_manager.show_statistics()
                case 8:
                    print("Goodbye")
                    running = False




    def run(self):
        self.display_menu()