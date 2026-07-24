from databaseManager import DatabaseManager
from financeManager import FinanceManager
from menu import Menu

databaseManager = DatabaseManager()
databaseManager.create_tables()
financeManager = FinanceManager(databaseManager)
financeManager.user_handler()
financeManager.initialize_default_categories()
financeManager.load_categories()
financeManager.load_transactions()

menu = Menu(financeManager)


if __name__ == "__main__":
    menu.run()

