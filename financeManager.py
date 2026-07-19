from transaction import Transaction
from databaseManager import DatabaseManager
from category import Category

class FinanceManager:

    def __init__(self):
        self.database_manager = DatabaseManager()
        self.transactions = []
        self.categories = [Category(1, "Food", "Expense"), Category(2, "Salary", "Income")]
        self.id = 0


    def input_amount(self):
        amount = int(input("Enter the amount: "))
        return amount


    def input_date(self):
        date = input("Enter the date: ")
        return date

    def input_type(self):
        type = input("Enter the type of the transaction (income/expense): ")
        return type
    def input_category(self):
        for i in self.categories:
            print(i.category_id, i.category_name, i.category_type)
            return i
        return None

    def input_string(self):
        description = input("Enter description: ")
        return description

    def generate_id(self):
        self.id+=1
        return self.id




    def add_transaction(self):
        transaction_type = self.input_type()
        amount = self.input_amount()
        date = self.input_date()
        category = self.input_category()
        description = self.input_string()
        transaction_id = self.generate_id()

        transaction = Transaction(transaction_id, transaction_type, amount, category, date, description)

        self.transactions.append(transaction)




    def show_transaction(self):
        for i in self.transactions:
            print(i.transaction_id, i.transaction_type)











