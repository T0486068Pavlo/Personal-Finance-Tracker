from databaseManager import DatabaseManager
from financeManager import FinanceManager
from menu import Menu
from sessionManager import SessionManager

databaseManager = DatabaseManager()
databaseManager.create_tables()
financeManager = FinanceManager(databaseManager)



menu = Menu(financeManager)
sessionManager = SessionManager(databaseManager, financeManager, menu)


if __name__ == "__main__":
    sessionManager.start()

