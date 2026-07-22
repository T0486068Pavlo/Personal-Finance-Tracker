from databaseManager import DatabaseManager
from financeManager import FinanceManager
from menu import Menu

databaseManager = DatabaseManager()
databaseManager.create_tables()
financeManager = FinanceManager(databaseManager)

menu = Menu(financeManager)


if __name__ == "__main__":
    menu.run()

