from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"
CATEGORIES = { "I": "Income", "E": "Expense" }

def get_date(prompt, allow_default=False):
    date_string = input(prompt)

    if allow_default and not date_string:
        return datetime.today().strftime(DATE_FORMAT)
    
    try:
        valid_date = datetime.strptime(date_string, DATE_FORMAT)
        return valid_date.strftime(DATE_FORMAT)
    except:
        print("Invalid date. Please use YYYY-MM-DD format")
        return get_date()

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category (I for income or E for expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    else:
        print("Invalid category. Please enter I or E")
        return get_category()



def get_description():
    desc = input("Enter the description (optional): ")
    if desc:
        return desc
    else:
        return None
