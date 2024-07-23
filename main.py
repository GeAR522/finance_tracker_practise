import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['Date', 'Amount', 'Category', 'Desc']
    DATE_FORMAT = "%Y-%m-%d"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Desc'])
            df.to_csv(cls.CSV_FILE, index=False)


    @classmethod
    def addEntry(cls, date, amount, category, desc):
        new_entry = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Desc": desc
        }
        with open(cls.CSV_FILE, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)


    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["Date"] = pd.to_datetime(df["Date"], format=CSV.DATE_FORMAT)
        df = df.sort_values(by="Date")
        start_date = datetime.strptime(start_date, CSV.DATE_FORMAT)
        end_date = datetime.strptime(end_date, CSV.DATE_FORMAT)
        
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.DATE_FORMAT)} to {end_date.strftime(CSV.DATE_FORMAT)}: "
            )
            print(filtered_df.to_string(index=False, formatters={"Date": lambda x: x.strftime(CSV.DATE_FORMAT)}))

            # We want the df, of only the entries where category is Income, then take amounts of that df, and sum them.
            total_income = filtered_df[filtered_df["Category"] == "Income"]["Amount"].sum()
            total_expense = filtered_df[filtered_df["Category"] == "Expense"]["Amount"].sum()
            print("Summary: ")
            print(f"Total Income: {total_income:.2f}")
            print(f"Total Expense: {total_expense:.2f}")
            print(f"Balance: {total_income - total_expense}")

        return filtered_df


        
def add():
    CSV.initialize_csv()
    date = get_date("Enter the date (YYYY-MM-DD): ", True)
    amount = get_amount()
    category = get_category()
    desc = get_description()
    CSV.addEntry(date, amount, category, desc)

def main():
    while True:
        print("\n 1. Add Transaction")
        print(" 2. View Transactions and Summary")
        print(" 3. Exit")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (YYYY-MM-DD): ", True)
            end_date = get_date("Enter the end date (YYYY-MM-DD): ", True)
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to plot the transactions? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")


def plot_transactions(df):
    df.set_index("Date", inplace=True)

    income_df = (
        df[df["Category"] == "Income"]
        .resample("D", level=0)
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["Category"] == "Expense"]
        .resample("D", level=0)
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 6))
    plt.plot(income_df.index, income_df["Amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["Amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income vs. Expense")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
