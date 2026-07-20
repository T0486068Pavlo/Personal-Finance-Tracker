from transaction import Transaction
from databaseManager import DatabaseManager
from category import Category
from datetime import datetime

class FinanceManager:

    def __init__(self):
        self.database_manager = DatabaseManager()
        self.transactions = []
        self.categories = [Category(1, "Food", "expense"),
                           Category(2, "Entertainment", "expense"),
                           Category(3, "Transport", "expense"),
                           Category(4, "Shopping", "expense"),
                           Category(5, "Housing", "expense"),
                           Category(6, "Education", "expense"),
                           Category(7, "Travel", "expense"),
                           Category(8, "Salary", "income"),
                           Category(9, "Gift", "income"),
                           Category(10, "Bonus", "income"),
                           Category(11, "Investment", "income"),
                           Category(12, "Freelance", "income")]
        self.id = 0




    # Helper methods to validate user input
    def input_amount(self, text):
        amount = ''
        valid = False
        while not valid:
            try:
                amount = int(input(text))
                valid = True
            except ValueError:
                print("Invalid input. Try again")


        return amount


    def input_date(self, text):
        date = ""
        valid = False
        while not valid:
            date_str = input(text)

            try:
                date = datetime.strptime(date_str, "%d/%m/%Y").date()
                valid = True
            except ValueError:
                print("Invalid date. Please use DD/MM/YYYY")
        return date

    def input_type(self, text):
        transaction_type = ""
        valid = False
        while not valid:
            transaction_type = input(text).lower().strip()
            if transaction_type not in ['income', 'expense']:
                print("Invalid input. Try again")
            else:
                valid = True

        return transaction_type

    def input_category(self, chosen_type, text):

        filtered = []

        for category in self.categories:
            if category.category_type == chosen_type:
                filtered.append(category)


        print(f"Categories for {chosen_type}: ")

        for index, category in enumerate (filtered, start = 1):
            print(f"{index}) {category}")

        valid = False
        valid_category =''
        while not valid:
            try:
                choice = int(input(text))
                num = choice - 1
                valid_category = filtered[num]

                valid = True
            except ValueError:
                print("Invalid input. Try again")
            except IndexError:
                print("This number is not in the list. Try again")

        return valid_category


    def input_description(self, text):
        description = input(text)
        if description == "":
            description = ""
        return description

    def generate_id(self):
        self.id+=1
        return self.id



    #Method that collects all data and creates a transaction object
    def add_transaction(self):
        transaction_type = self.input_type("Enter transaction type (Income/Expense): ")
        amount = self.input_amount("Enter amount: £")
        date = self.input_date("Enter a date (DD/MM/YYYY): ")
        category = self.input_category(transaction_type, "Enter the number from the list: ")
        description = self.input_description("Enter description or leave empty (optional): ")
        transaction_id = self.generate_id()
        transaction = Transaction(transaction_id, transaction_type, amount, category, date, description)

        self.transactions.append(transaction)


    def list_transactions(self):
        if self.transactions:
            for transaction in self.transactions:
                print(f"|ID: {transaction.transaction_id}| {transaction.transaction_type} for £{transaction.amount} in '{transaction.category}' from {transaction.date.strftime("%d/%m/%Y")}")
                if transaction.description:
                    print(f"Description: {transaction.description}")
                print()
        else:
            print("There are no transactions yet")



    def delete_transaction(self):
        pass











