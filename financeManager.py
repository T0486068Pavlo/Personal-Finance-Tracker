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

    def generate_id(self):
        self.id+=1
        return self.id

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



    #Method that collects all data and creates a transaction object
    def add_transaction(self):
        transaction_type = self.input_type("Enter transaction type (Income/Expense): ")
        amount = self.input_integer("Enter amount: £")
        date = self.input_date("Enter a date (DD/MM/YYYY): ")
        category = self.input_category(transaction_type, "Enter the number from the list: ")
        description = self.input_description("Enter description or leave empty (optional): ")
        transaction_id = self.generate_id()
        transaction = Transaction(transaction_id, transaction_type, amount, category, date, description)

        self.transactions.append(transaction)


    def list_transactions(self):

        if self.transactions:
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
                    f"{transaction.description or '-'}"
                )
        else:
            print("There are no transactions yet")



    def delete_transaction(self):
        self.list_transactions()

        found_transaction = self.find_transaction_by_id("Enter the ID of the transaction to delete: ")

        confirmation = self.input_confirmation("Please confirm the deletion (Y/N): ")
        if confirmation:
            self.transactions.remove(found_transaction)
            print(f"Transaction with ID: {found_transaction.transaction_id} from ({found_transaction.transaction_type}) deleted")
        else:
            print("Deletion cancelled")






    def edit_transaction(self):

        self.list_transactions()

        found_transaction = self.find_transaction_by_id("Enter the ID of the transaction to edit: ")
        running = True
        while running:
            print(f"Current transaction: \n")
            print(f"Type: {found_transaction.transaction_type}")
            print(f"Amount: {found_transaction.amount}")
            print(f"Category: {found_transaction.category}")
            print(f"Date: {found_transaction.date.strftime("%d/%m/%Y")}")
            print(f"Description: {found_transaction.description or "-"}\n")


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
                    for trans in self.transactions:
                        if trans.transaction_type == find_type:
                            print(f"ID: {trans.transaction_id}| "
                                  f"Type: {trans.transaction_type}| "
                                  f"Category: {trans.category}| "
                                  f"Amount: {trans.amount}| "
                                  f"Date: {trans.date}| "
                                  f"Description: {trans.description or "-"}")
                        else:
                            print(f"No transactions for {find_type}")

                case 3:
                    trans_type_find = self.input_type("Enter type of the transaction (Income/Expense): ")
                    find_category = self.input_category(trans_type_find,"Enter category to search for: " )
                    for trans in self.transactions:
                        if trans.category == find_category:
                            print(f"ID: {trans.transaction_id}| "
                                  f"Type: {trans.transaction_type}| "
                                  f"Category: {trans.category}| "
                                  f"Amount: {trans.amount}| "
                                  f"Date: {trans.date}| "
                                  f"Description: {trans.description or "-"}")
                        else:
                            print(f"No transactions for {find_category}")

                case 4:
                    min_amount = self.input_integer("Enter the minimum amount for range: ")
                    max_amount= self.input_integer("Enter the maximum amount for range: ")

                    for trans in self.transactions:
                        if  min_amount <= trans.amount <= max_amount:
                            print(f"ID: {trans.transaction_id}| "
                                  f"Type: {trans.transaction_type}| "
                                  f"Category: {trans.category}| "
                                  f"Amount: {trans.amount}| "
                                  f"Date: {trans.date}| "
                                  f"Description: {trans.description or "-"}")
                        else:
                            print("No transaction found")
                case 5:
                    find_date = self.input_date("Enter date to find transaction: ")
                    for trans in self.transactions:
                        if trans.date == find_date:
                            print(f"ID: {trans.transaction_id}| "
                                  f"Type: {trans.transaction_type}| "
                                  f"Category: {trans.category}| "
                                  f"Amount: {trans.amount}| "
                                  f"Date: {trans.date}| "
                                  f"Description: {trans.description or "-"}")
                        else:
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
                    cat_name = input("Enter category name: ")
                    largest_id = 0
                    for i in self.categories:
                        if i.category_id > largest_id:
                            largest_id = i.category_id
                    new_id = largest_id +1
                    print(f" Category -> ID: {new_id}| Name: {cat_name}| Type: {cat_type} added")
                    self.categories.append(Category(new_id, cat_name,cat_type))

                    self.list_categories()

                case 3:
                    self.list_categories()
                    found = False
                    #here I check if category with entered ID even exists
                    category_to_delete = self.find_category_by_id("Enter the ID of category to delete: ")
                    #here i look through transactions
                    for transaction in self.transactions:
                        if transaction.category == category_to_delete:
                            found = True






                    if not found:
                        confirmation = self.input_confirmation("Are you sure to delete (Y/N):  ")
                        if confirmation:
                            self.categories.remove(category_to_delete)
                            self.list_categories()

                    else:
                        print("This category contains transaction. Cannot be deleted")



                case 4:
                    running = False
                case _:
                    print("Invalid input")
































