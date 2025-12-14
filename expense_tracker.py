import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

# CSV file setup
FILE_NAME = "expenses.csv"

# Create file with header and sample data if not exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Type", "Category", "Amount", "Description"])
        # Sample data
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), "Income", "Income", 5000.0, "Freelance Work"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), "Expense", "Food", 150.0, "Lunch"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), "Expense", "Transport", 100.0, "Bus Fare"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), "Expense", "Rent", 12000.0, "December Rent"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), "Income", "Income", 2000.0, "Part-time Job"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), "Expense", "Food", 200.0, "Dinner"])

# Add Income function
def add_income():
    try:
        amount = float(input("Enter income amount: ₹"))
        if amount <= 0 or amount > 1e7:
            print("Please enter a realistic amount (0-10,000,000)")
            return
        description = input("Enter description: ")
        date = datetime.now().strftime("%Y-%m-%d")
        type_income = "Income"
        category = "Income"

        with open(FILE_NAME, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, type_income, category, amount, description])

        print(f"Income of ₹{amount} added successfully!")
    except ValueError:
        print("Invalid amount! Please enter a number.")

# Add Expense function
def add_expense():
    try:
        amount = float(input("Enter expense amount: ₹"))
        if amount <= 0 or amount > 1e7:
            print("Please enter a realistic amount (0-10,000,000)")
            return
        category = input("Enter category (Food, Rent, Travel, etc.): ")
        description = input("Enter description: ")
        date = datetime.now().strftime("%Y-%m-%d")
        type_expense = "Expense"

        with open(FILE_NAME, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, type_expense, category, amount, description])

        print(f"Expense of ₹{amount} added successfully!")
    except ValueError:
        print("Invalid amount! Please enter a number.")

# View Summary
def view_summary():
    total_income = 0
    total_expense = 0

    if not os.path.exists(FILE_NAME):
        print("No data available yet!")
        return

    with open(FILE_NAME, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                amount = float(row["Amount"])
            except ValueError:
                continue
            if row["Type"] == "Income":
                total_income += amount
            elif row["Type"] == "Expense":
                total_expense += amount

    balance = total_income - total_expense

    print("\n===== SUMMARY =====")
    print(f"Total Income : ₹{total_income}")
    print(f"Total Expense: ₹{total_expense}")
    print(f"Balance      : ₹{balance}")

# Category-wise Report
def category_report():
    category_totals = {}

    if not os.path.exists(FILE_NAME):
        print("No data available yet!")
        return

    with open(FILE_NAME, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Type"] == "Expense":
                category = row["Category"]
                try:
                    amount = float(row["Amount"])
                except ValueError:
                    continue
                category_totals[category] = category_totals.get(category, 0) + amount

    if not category_totals:
        print("No expense data available!")
        return

    print("\n===== CATEGORY-WISE EXPENSE =====")
    for cat, amt in category_totals.items():
        print(f"{cat}: ₹{amt}")

    plt.figure(figsize=(6,6))
    plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%')
    plt.title("Expenses by Category")
    plt.show()

# Monthly Report
def monthly_report():
    monthly_income = {}
    monthly_expense = {}

    if not os.path.exists(FILE_NAME):
        print("No data available yet!")
        return

    with open(FILE_NAME, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            month = row["Date"][:7]  # YYYY-MM
            try:
                amount = float(row["Amount"])
            except ValueError:
                continue
            if row["Type"] == "Income":
                monthly_income[month] = monthly_income.get(month, 0) + amount
            elif row["Type"] == "Expense":
                monthly_expense[month] = monthly_expense.get(month, 0) + amount

    all_months = sorted(set(list(monthly_income.keys()) + list(monthly_expense.keys())))
    if not all_months:
        print("No data available for monthly report!")
        return

    print("\n===== MONTHLY REPORT =====")
    for month in all_months:
        income = monthly_income.get(month,0)
        expense = monthly_expense.get(month,0)
        balance = income - expense
        print(f"{month} → Income: ₹{income}, Expense: ₹{expense}, Balance: ₹{balance}")

    plt.figure(figsize=(8,5))
    plt.bar(all_months, [monthly_income.get(m,0) for m in all_months], label="Income", alpha=0.7)
    plt.bar(all_months, [monthly_expense.get(m,0) for m in all_months], label="Expense", alpha=0.7)
    plt.title("Monthly Income vs Expense")
    plt.xlabel("Month")
    plt.ylabel("Amount (₹)")
    plt.legend()
    plt.show()

# Step 9a: Search by Date or Category
def search_transactions():
    if not os.path.exists(FILE_NAME):
        print("No data available yet!")
        return

    print("\nSearch by:")
    print("1. Date (YYYY-MM-DD)")
    print("2. Category")
    choice = input("Enter choice (1-2): ")

    if choice == "1":
        date_search = input("Enter date (YYYY-MM-DD): ")
        print(f"\nTransactions on {date_search}:")
    elif choice == "2":
        category_search = input("Enter category: ").lower()
        print(f"\nTransactions in category '{category_search}':")
    else:
        print("Invalid choice!")
        return

    found = False
    with open(FILE_NAME, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                amount = float(row["Amount"])
            except ValueError:
                continue
            if choice == "1" and row["Date"] == date_search:
                print(f"{row['Date']} | {row['Type']} | {row['Category']} | ₹{amount} | {row['Description']}")
                found = True
            elif choice == "2" and row["Category"].lower() == category_search:
                print(f"{row['Date']} | {row['Type']} | {row['Category']} | ₹{amount} | {row['Description']}")
                found = True

    if not found:
        print("No transactions found.")

# Step 9b: Export filtered report to CSV
def export_report():
    if not os.path.exists(FILE_NAME):
        print("No data available yet!")
        return

    export_file = input("Enter filename to export (e.g., report.csv): ")
    print("\nFilter transactions to export:")
    print("1. All Transactions")
    print("2. By Date")
    print("3. By Category")
    choice = input("Enter choice (1-3): ")

    filtered_rows = []
    with open(FILE_NAME, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                amount = float(row["Amount"])
            except ValueError:
                continue
            if choice == "1":
                filtered_rows.append(row)
            elif choice == "2":
                date_search = input("Enter date (YYYY-MM-DD): ")
                if row["Date"] == date_search:
                    filtered_rows.append(row)
            elif choice == "3":
                category_search = input("Enter category: ").lower()
                if row["Category"].lower() == category_search:
                    filtered_rows.append(row)

    if not filtered_rows:
        print("No data to export!")
        return

    with open(export_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Type", "Category", "Amount", "Description"])
        writer.writeheader()
        writer.writerows(filtered_rows)

    print(f"Report exported successfully to '{export_file}'")

# Menu function
def menu():
    while True:
        print("\n===== EXPENSE TRACKER MENU =====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. Category-wise Report")
        print("5. Monthly Report")
        print("6. Exit")
        print("7. Search Transactions")
        print("8. Export Report to CSV")

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            add_income()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_summary()
        elif choice == "4":
            category_report()
        elif choice == "5":
            monthly_report()
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        elif choice == "7":
            search_transactions()
        elif choice == "8":
            export_report()
        else:
            print("Invalid choice. Please enter 1-8.")

# Run the program
menu()
