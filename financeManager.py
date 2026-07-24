from transaction import Transaction
from databaseManager import DatabaseManager
from category import Category
from datetime import datetime
import sqlite3

from user import User

DEFAULT_CATEGORIES = [
    ("Food", "expense"),
    ("Entertainment", "expense"),
    ("Transport", "expense"),
    ("Shopping", "expense"),
    ("Housing", "expense"),
    ("Education", "expense"),
    ("Travel", "expense"),
    ("Salary", "income"),
    ("Gift", "income"),
    ("Bonus", "income"),
    ("Investment", "income"),
    ("Freelance", "income"),
]


class FinanceManager:

    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.transactions = []
        self.categories = []
        # self.id = 0



    # Helper methods to validate user input

    def input_integer(self, text):
        amount = ''
        valid = False
        while not valid:
            try:
                amount = int(input(text))
                if amount < 0:
                    print("Cannot be less than 0. Try again")
                else:
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

    # def generate_id(self):
    #     self.id+=1
    #     return self.id

    def input_confirmation(self, text):
        valid = False
        confirmation = ''
        while not valid:
            choice = input(text)
            if choice in ['y', 'Y']:
                confirmation = True
                valid = True
            elif choice in ['n', 'N']:
                confirmation = False
                valid = True
            else:
                print("Invalid input. Try again")

        return confirmation


    def find_transaction_by_id(self, text):
        found_transaction = ''
        if self.transactions:
            valid = False
            found = False
            while not valid:
                try:
                    choice = int(input(text))
                    for transaction in self.transactions:
                        if transaction.transaction_id == choice:
                            found_transaction = transaction
                            found = True
                            break
                    if not found:
                        print("This ID does not exist")
                    else:
                        valid = True
                except ValueError:
                    print("Invalid input. Try again")

        return found_transaction

        # Helper function to display details of transaction

    def display_info(self, trans):
        print(f"ID: {trans.transaction_id}")
        print(f"Type: {trans.transaction_type}")
        print(f"Amount: {trans.amount}")
        print(f"Category: {trans.category}")
        print(f"Date: {trans.date.strftime("%d/%m/%Y")}")
        print(f"Description: {trans.description or "-"}\n")
        print()

    def check_if_empty(self):
        found = False
        if self.transactions:
            found = True
        else:
            print()
            print("There are no transactions yet")
            print()

        return found





    #Method that collects all data and creates a transaction object
    def add_transaction(self):
        transaction_type = self.input_type("Enter transaction type (Income/Expense): ")
        amount = self.input_integer("Enter amount: £")
        date = self.input_date("Enter a date (DD/MM/YYYY): ")
        category = self.input_category(transaction_type, "Enter the number from the list: ")
        description = self.input_description("Enter description or leave empty (optional): ")


        #Database insertion
        category_id = category.category_id
        new_id = self.database_manager.add_transaction(transaction_type, amount, category_id, date, description, self.user.user_id)


        #List insertion
        transaction = Transaction(new_id, transaction_type, amount, category, date, description)
        self.transactions.append(transaction)


    def list_transactions(self):

        if self.check_if_empty():
            print("=" * 95)
            print(f"{'ID':<5} {'Type':<12} {'Amount':>10} {'Category':<18} {'Date':<15} {'Description':<25}")
            print("=" * 95)
            for transaction in self.transactions:
                print(
                    f"{transaction.transaction_id:<5} "
                    f"{transaction.transaction_type:<12} "
                    f"£{transaction.amount:>11.2f} "
                    f"{transaction.category.category_name:<18} "
                    f"{transaction.date.strftime("%d/%m/%Y"):<15} "
                    f"{transaction.description or '-'}")





    def delete_transaction(self):


        if self.check_if_empty():
            self.list_transactions()
            found_transaction = self.find_transaction_by_id("Enter the ID of the transaction to delete: ")

            confirmation = self.input_confirmation("Please confirm the deletion (Y/N): ")
            if confirmation:
                self.transactions.remove(found_transaction)
                print(f"Transaction with ID: {found_transaction.transaction_id} from ({found_transaction.transaction_type}) deleted")
            else:
                print("Deletion cancelled")





    def edit_transaction(self):


        if self.check_if_empty():
            self.list_transactions()
            found_transaction = self.find_transaction_by_id("Enter the ID of the transaction to edit: ")
            running = True
            while running:
                self.display_info(found_transaction)


                print("What would yoy like to edit: ")
                print("1. Amount")
                print("2. Category")
                print("3. Date")
                print("4. Description")
                print("5. Cancel")

                choice = self.input_integer("Enter the number from the menu: ")

                match choice:

                    case 1:
                        new_amount = self.input_integer("Enter the new amount: ")
                        if new_amount == found_transaction.amount:
                            print("No changes were made")
                        else:
                            found_transaction.amount = new_amount
                            print(f"Amount changed to {new_amount}\n")
                    case 2:
                        new_category = self.input_category(found_transaction.transaction_type,"Enter new category: ")
                        if new_category == found_transaction.category:
                            print("No changes were made")
                        else:
                            found_transaction.category = new_category
                            print(f"Category changed to {new_category}\n")
                    case 3:
                        new_date = self.input_date("Enter new date (DD/MM/YYYY): ")
                        if new_date == found_transaction.date:
                            print("No changes were made")
                        else:
                            found_transaction.date = new_date
                            print(f"Date changed to {new_date.strftime("%d/%m/%Y")}\n")
                    case 4:
                        new_description = self.input_description("Enter new description: ")
                        found_transaction.description = new_description
                        print(f"Description changed to {new_description}\n")

                    case 5:
                        print("Transaction updated\n")
                        running = False
                    case _:
                        print("Invalid input")


    def search_transaction(self):

        if self.check_if_empty():
            print("Search transactions: ")


            running = True
            while running:
                print("1. By ID")
                print("2. By Type")
                print("3. By Category")
                print("4. By Amount")
                print("5. By Date")
                print("6. Cancel")
                print()


                choice = self.input_integer("Enter your choice: ")

                match choice:
                    case 1:
                        find_id = self.find_transaction_by_id("Enter the ID of the transaction to find: ")
                        print(f"ID: {find_id.transaction_id}| "
                              f"Type: {find_id.transaction_type}|"
                              f"Category: {find_id.category}|"
                              f"Amount: {find_id.amount}|"
                              f"Date: {find_id.date}|"
                              f"Description {find_id.description or "-"}")
                    case 2:
                        find_type = self.input_type("Enter type of the transaction (Income/Expense): ")
                        found = False
                        for trans in self.transactions:
                            if trans.transaction_type == find_type:
                                found = True
                                print(f"ID: {trans.transaction_id}| "
                                      f"Type: {trans.transaction_type}| "
                                      f"Category: {trans.category}| "
                                      f"Amount: {trans.amount}| "
                                      f"Date: {trans.date}| "
                                      f"Description: {trans.description or "-"}")
                        if not found:
                            print(f"No transactions for {find_type}")


                    case 3:
                        trans_type_find = self.input_type("Enter type of the transaction (Income/Expense): ")
                        find_category = self.input_category(trans_type_find,"Enter category to search for: " )
                        found = False
                        for trans in self.transactions:
                            if trans.category == find_category:
                                found = True
                                print(f"ID: {trans.transaction_id}| "
                                      f"Type: {trans.transaction_type}| "
                                      f"Category: {trans.category}| "
                                      f"Amount: {trans.amount}| "
                                      f"Date: {trans.date}| "
                                      f"Description: {trans.description or "-"}")
                        if not found:
                            print(f"No transactions for {find_category}")


                    case 4:
                        min_amount = self.input_integer("Enter the minimum amount for range: ")
                        max_amount= self.input_integer("Enter the maximum amount for range: ")
                        found = False

                        for trans in self.transactions:
                            if  min_amount <= trans.amount <= max_amount:
                                found = True
                                print(f"ID: {trans.transaction_id}| "
                                      f"Type: {trans.transaction_type}| "
                                      f"Category: {trans.category}| "
                                      f"Amount: {trans.amount}| "
                                      f"Date: {trans.date}| "
                                      f"Description: {trans.description or "-"}")
                        if not found:
                            print("No transaction found")

                    case 5:
                        find_date = self.input_date("Enter date to find transaction: ")
                        found = False
                        for trans in self.transactions:
                            if trans.date == find_date:
                                found = True
                                print(f"ID: {trans.transaction_id}| "
                                      f"Type: {trans.transaction_type}| "
                                      f"Category: {trans.category}| "
                                      f"Amount: {trans.amount}| "
                                      f"Date: {trans.date}| "
                                      f"Description: {trans.description or "-"}")
                        if not found:
                            print(f"No transaction found for {find_date}")

                    case 6:
                        running = False

                    case _:
                        print("Invalid input")


    def list_categories(self):
        for category in self.categories:
            print(f"|ID {category.category_id}| {category} | {category.category_type}")
            print()



    def find_category_by_id(self, text):
        found_category = ''
        if self.categories:
            valid = False
            found = False
            while not valid:
                try:
                    choice = int(input(text))
                    for category in self.categories:
                        if category.category_id == choice:
                            found_category = category
                            found = True
                            break
                    if not found:
                        print("Category with this ID does not exist")
                    else:
                        valid = True
                except ValueError:
                    print("Invalid input. Try again")
        return found_category

    def input_category_name(self, text):
        new_name = ''
        running = True

        while running:
            valid = True
            new_name = input(text).strip().capitalize()
            if new_name == '':
                print("Cannot be empty. Try again")
                continue

            for category in self.categories:
                if category.category_name == new_name:
                    print(f"Category '{new_name}' already exists")
                    valid = False
                    break

            if valid:
                running = False

        return new_name










    def manage_categories(self):

        print("Manage categories: ")
        running = True
        while running:
            print("1. View Categories")
            print("2. Add Category")
            print("3. Delete Category")
            print("4. Cancel")
            print()
            choice = self.input_integer("Enter the number from the menu: ")

            match choice:

                case 1:
                    self.list_categories()
                case 2:
                    cat_type = self.input_type("Enter category type (Income/Expense): ")
                    cat_name = self.input_category_name("Enter category name: ")
                    new_id = self.database_manager.add_category(cat_name, cat_type, self.user.user_id)


                    print(f" Category -> ID: {new_id}| Name: {cat_name}| Type: {cat_type} added")
                    self.categories.append(Category(new_id, cat_name,cat_type))

                    self.list_categories()

                case 3:
                    self.list_categories()

                    category_to_delete = self.find_category_by_id("Enter the ID of category to delete: ")

                    confirmation = self.input_confirmation("Are you sure to delete (Y/N):  ")
                    if confirmation:
                       try:
                           self.database_manager.delete_category(category_to_delete.category_id)
                           self.categories.remove(category_to_delete)
                           print(f"Category '{category_to_delete}' deleted successfully")
                           self.list_categories()

                       except sqlite3.IntegrityError:
                           print("This category cannot be deleted. It contains transactions")

                    else:
                        print("Deletion cancelled")



                case 4:
                    running = False
                case _:
                    print("Invalid input")





    def show_statistics(self):
        total_income = 0
        total_expense = 0
        income_transactions = 0
        expense_transactions = 0
        largest_income = -1
        largest_expense = -1
        largest_expense_transaction = None
        largest_income_transaction = None

        for trans in self.transactions:
            if trans.transaction_type == "income":
                total_income +=trans.amount
                income_transactions +=1
                if trans.amount > largest_income:
                    largest_income = trans.amount
                    largest_income_transaction = trans

            elif trans.transaction_type == "expense":
                total_expense +=trans.amount
                expense_transactions +=1
                if trans.amount > largest_expense:
                    largest_expense = trans.amount
                    largest_expense_transaction = trans








        print("-"*95)
        print("Statistics")
        print("="*95)
        print(f"Total income: £{total_income}")
        print(f"Total expense: £{total_expense}")
        print(f"Current balance: £{total_income-total_expense}")
        print(f"Income transactions: {income_transactions}")
        print(f"Expense transactions: {expense_transactions}")
        print()
        if largest_income_transaction is not None:
            print(f"Largest income: ")
            self.display_info(largest_income_transaction)
        if largest_expense_transaction is not None:
            print(f"Largest expense: ")
            self.display_info(largest_expense_transaction)


        total = 0
        most_expensive_category = None
        biggest_total = 0

        print("Spending of each category: ")
        if self.transactions:
            for c in self.categories:
                for t in self.transactions:
                    if t.category == c:
                        total+=t.amount
                if total !=0:
                    print(f"Category: {c} | Total: £{total}")
                if total > biggest_total:
                    biggest_total = total
                    most_expensive_category = c
                total = 0

            print(f"Most expensive category: {most_expensive_category} £({biggest_total})")
        else:
            print("No spending statistic available yet")



        print("="*95)




    #DATABASE METHODS

    # DatabaseManager helper method
    def close_database(self):
        self.database_manager.close_connection()



    #Method for database to create or load user profile

    def user_handler(self):
        row = self.database_manager.get_user()
        if row is None:
            name = input("Enter your name: ")
            currency = input("Enter your preferable currency: ")
            balance = self.input_integer("Enter your initial balance: ")

            user_id = self.database_manager.insert_user(name, currency, balance)

            self.user = User(user_id, name, currency, balance)
        else:
            self.user = User(row["user_id"],row["username"], row["currency"], row["initial_balance"])

    def initialize_default_categories(self):
        self.database_manager.initialize_categories(DEFAULT_CATEGORIES, self.user.user_id)

    def load_categories(self):
        categories = self.database_manager.load_categories(self.user.user_id)

        self.categories.clear()
        for c in categories:
            category_id = c["category_id"]
            category_name = c["category_name"]
            category_type = c["category_type"]
            category = Category(category_id, category_name,category_type )
            self.categories.append(category)


    def find_category_database(self, cat_id):
        found_category = ''
        if self.categories:
            valid = False
            found = False
            while not valid:
                try:
                    for category in self.categories:
                        if category.category_id == cat_id:
                            found_category = category
                            found = True
                            break
                    if not found:
                        print("Category with this ID does not exist")
                    else:
                        valid = True
                except ValueError:
                    print("Invalid input. Try again")
        return found_category



    def load_transactions(self):
        transactions = self.database_manager.load_transactions(self.user.user_id)
        self.transactions.clear()

        for t in transactions:
            transaction_id = t["transaction_id"]
            transaction_type = t["transaction_type"]
            amount = t["amount"]
            category_id = t["category_id"]
            date= t["date"]
            description = t["description"]

            date = datetime.strptime(date, "%Y-%m-%d")
            category_obj = self.find_category_database(category_id)
            transaction = Transaction(transaction_id, transaction_type, amount,category_obj, date, description)
            self.transactions.append(transaction)









































