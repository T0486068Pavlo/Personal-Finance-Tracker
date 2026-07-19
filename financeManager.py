from transaction import Transaction
from databaseManager import DatabaseManager
from category import Category

class FinanceManager:

    def __init__(self):
        self.database_manager = DatabaseManager()
        self.transactions = []
        self.categories = [Category(1, "Food", "expense"), Category(2, "Salary", "income")]
        self.id = 0


    def input_amount(self):
        amount = int(input("Enter the amount: "))
        return amount


    def input_date(self):
        date = input("Enter the date: ")
        return date

    def input_type(self):
        transaction_type = ""
        valid = True
        while valid:
            transaction_type = input("Enter transaction type (income/expense): ").lower().strip()
            if transaction_type not in ['income', 'expense']:
                print("Invalid input. Try again")
            else:
                valid = False

        return transaction_type

    def input_category(self, chosen_type):

        filtered = []

        for category in self.categories:
            if category.category_type == chosen_type:
                filtered.append(category)

        for index, category in enumerate (filtered, start = 1):
            print(f"{index}) {category}")

        choice = int(input("Enter the number from the list: "))
        num = choice -1

        return filtered[num]







    def input_description(self):
        description = input("Enter description or leave empty (optional): ")
        if description == "":
            description = ""
        return description

    def generate_id(self):
        self.id+=1
        return self.id




    def add_transaction(self):
        transaction_type = self.input_type()
        amount = self.input_amount()
        date = self.input_date()
        category = self.input_category(transaction_type)
        description = self.input_description()
        transaction_id = self.generate_id()

        transaction = Transaction(transaction_id, transaction_type, amount, category, date, description)

        self.transactions.append(transaction)




    def show_transaction(self):
        for transaction in self.transactions:
            print(f"ID: {transaction.transaction_id}) {transaction.transaction_type} for £{transaction.amount} in {transaction.category} from {transaction.date}")
            if transaction.description:
                print(f"Description: {transaction.description}")
            print()











