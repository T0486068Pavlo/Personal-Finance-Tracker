from financeManager import FinanceManager
from menu import Menu


financeManager = FinanceManager()

menu = Menu(financeManager)


if __name__ == "__main__":
    menu.run()

