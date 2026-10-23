
import csv
from datetime import datetime
from collections import defaultdict

FILE = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]



def load_expenses():
    try:
        with open(FILE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            # Handle an empty file
            if reader.fieldnames is None:
                return []

            # Remove spaces from column names
            reader.fieldnames = [
                name.strip().lower() if name else name
                for name in reader.fieldnames
            ]

            # Check that the expected columns exist
            if not all(field in reader.fieldnames for field in FIELDS):
                print("Error: expenses.csv has an incorrect header.")
                print("Expected:", ",".join(FIELDS))
                print("Found:", reader.fieldnames)
                return []

            return list(reader)

    except FileNotFoundError:
        with open(FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
        return []



def save_expense(row):
    try:
        with open(FILE, "r", newline="", encoding="utf-8") as file:
            has_header = file.readline().strip() == ",".join(FIELDS)
    except FileNotFoundError:
        has_header = False

    with open(FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if not has_header:
            writer.writeheader()
        writer.writerow(row)


def add_expense():
    while True:
        date_text = input("Date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date. Example: 2026-10-23")

    category = input("Category: ").strip().title()
    if not category:
        print("Category cannot be empty.")
        return

    description = input("Description: ").strip()
    if not description:
        print("Description cannot be empty.")
        return

    while True:
        try:
            amount = float(input("Amount: "))
            if amount < 0:
                print("Amount cannot be negative.")
                continue
            break
        except ValueError:
            print("Enter a valid numeric amount.")

    row = {
        "date": date_text,
        "category": category,
        "description": description,
        "amount": f"{amount:.2f}",
    }

    save_expense(row)
    print("Expense saved successfully!")



def view_expenses(rows):
    valid_rows = []

    for row in rows:
        # Skip repeated CSV header rows
        if (row.get("date") or "").strip().lower() == "date":
            continue

        try:
            float(row["amount"])
            valid_rows.append(row)
        except (ValueError, TypeError, KeyError):
            print("Skipping an invalid expense record:", row)

    if not valid_rows:
        print("No valid expenses found.")
        return

    print("\nDate        Category     Description              Amount")
    print("-" * 65)

    for row in valid_rows:
        print(
            f"{row['date']:<12}"
            f"{row['category']:<13}"
            f"{row['description'][:23]:<24}"
            f"{float(row['amount']):>8.2f}"
        )



def filter_expenses():
    rows = load_expenses()
    print("1. Filter by category")
    print("2. Filter by month")

    choice = input("Choose filter: ").strip()

    if choice == "1":
        category = input("Category: ").strip().casefold()
        results = [
            row for row in rows
            if row["category"].casefold() == category
        ]
    elif choice == "2":
        month = input("Month (YYYY-MM): ").strip()
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Enter the month in YYYY-MM format.")
            return

        results = [
            row for row in rows
            if row["date"].startswith(month)
        ]
    else:
        print("Invalid filter.")
        return

    view_expenses(results)



def show_summary():
    rows = load_expenses()

    # Remove repeated headers and invalid records
    valid_rows = []

    for row in rows:
        try:
            if row.get("date", "").strip().lower() == "date":
                continue

            amount = float(row["amount"])
            valid_rows.append((row, amount))

        except (ValueError, TypeError, KeyError):
            continue

    if not valid_rows:
        print("No expenses available.")
        return

    totals = defaultdict(float)
    grand_total = 0.0
    biggest = None
    biggest_amount = 0.0

    for row, amount in valid_rows:
        category = row["category"]
        totals[category] += amount
        grand_total += amount

        if biggest is None or amount > biggest_amount:
            biggest = row
            biggest_amount = amount

    print("\n--- Expense Summary ---")

    for category, total in sorted(totals.items()):
        print(f"{category:<15} {total:>10.2f}")

    print("-" * 28)
    print(f"{'Grand Total':<15} {grand_total:>10.2f}")

    if biggest:
        print(
            "Largest expense:",
            biggest["description"],
            f"({biggest_amount:.2f})"
        )



def main():
    load_expenses()

    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Filter expenses")
        print("4. Summary")
        print("5. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses(load_expenses())
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Choose 1 to 5.")


if __name__ == "__main__":
    main()
