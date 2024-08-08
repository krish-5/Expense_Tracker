import tkinter as tk 
from tkinter import ttk, messagebox, simpledialog
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from datetime import datetime

class ExpenseTrackerApp(tk.Tk):
   
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("1300x600")
        self.expenses = []
        self.categories = [
            "Food",
            "Transportation",
            "Utilities",
            "Entertainment",
            "Other",
        ]
        self.category_var = tk.StringVar(self)
        self.category_var.set(self.categories[0])
        self.create_widgets()

    def create_widgets(self):
        # headerrr
        self.label = tk.Label(
            self, text="Expense Tracker", font=("Helvetica", 20, "bold"), bg="#3f51b5", fg="white"
        )
        self.label.pack(pady=10, fill=tk.X)
       
        self.frame_input = tk.Frame(self, bg="#f0f0f0")
        self.frame_input.pack(pady=10)

        # Expense entry 
        
        # 1
        self.expense_label = tk.Label(
            self.frame_input, text="Expense Amount:", font=("Helvetica", 12), bg="#f0f0f0"
        )
        self.expense_label.grid(row=0, column=0, padx=5)
        
        self.expense_entry = tk.Entry(
            self.frame_input, font=("Helvetica", 12), width=15
        )
        self.expense_entry.grid(row=0, column=1, padx=5)


         # 2
        self.item_label = tk.Label(
            self.frame_input, text="Item Description:", font=("Helvetica", 12), bg="#f0f0f0"
        )
        self.item_label.grid(row=0, column=2, padx=5)
        self.item_entry = tk.Entry(self.frame_input, font=("Helvetica", 12), width=20)
        self.item_entry.grid(row=0, column=3, padx=5)


        # 3
        self.category_label = tk.Label(
            self.frame_input, text="Category:", font=("Helvetica", 12), bg="#f0f0f0"
        )
        self.category_label.grid(row=0, column=4, padx=5)
        self.category_dropdown = ttk.Combobox(
            self.frame_input,
            textvariable=self.category_var,
            values=self.categories,
            font=("Helvetica", 12),
            width=15,
        )
        self.category_dropdown.grid(row=0, column=5, padx=5)


        # 4
        self.date_label = tk.Label(
            self.frame_input, text="Date (YYYY-MM-DD):", font=("Helvetica", 12), bg="#f0f0f0"
        )
        self.date_label.grid(row=0, column=6, padx=5)
        self.date_entry = tk.Entry(self.frame_input, font=("Helvetica", 12), width=15)
        self.date_entry.grid(row=0, column=7, padx=5)



        self.date_entry.bind("<FocusIn>", self.set_today_date)

        self.set_today_date(None)

        self.add_button = tk.Button(self, text="Add Expense", command=self.add_expense, bg="#3f51b5", fg="white")
        self.add_button.pack(pady=5)

        self.frame_list = tk.Frame(self, bg="#f0f0f0")
        self.frame_list.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self.frame_list)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.expense_listbox = tk.Listbox(
            self.frame_list,
            font=("Helvetica", 12),
            width=70,
            yscrollcommand=self.scrollbar.set,
        )
        self.expense_listbox.pack(pady=5)
        self.scrollbar.config(command=self.expense_listbox.yview)

        self.edit_button = tk.Button(
            self, text="Edit Expense", command=self.edit_expense, bg="#3f51b5", fg="white"
        )
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(
            self, text="Delete Expense", command=self.delete_expense, bg="#3f51b5", fg="white"
        )
        self.delete_button.pack(pady=5)

        self.save_button = tk.Button(
            self, text="Save Expenses", command=self.save_expenses, bg="#3f51b5", fg="white"
        )
        self.save_button.pack(pady=5)

        self.total_label = tk.Label(
            self, text="Today's Expenses:", font=("Helvetica", 12), bg="#f0f0f0"
        )
        self.total_label.pack(pady=5)

        self.show_chart_button = tk.Button(
            self, text="Show Expenses Chart", command=self.show_expenses_chart, bg="#3f51b5", fg="white"
        )
        self.show_chart_button.pack(pady=5)

        self.show_monthly_expenses_button = tk.Button(
            self, text="Total Expenses", command=self.calculate_total_monthly_expenses, bg="#3f51b5", fg="white"
        )
        self.show_monthly_expenses_button.pack(pady=5)


    def add_expense(self):
        expense = self.expense_entry.get()
        item = self.item_entry.get()
        category = self.category_var.get()
        date = self.date_entry.get()

        # Check if expense and date are not empty
        if expense and date:
            self.expenses.append((expense, item, category, date))
            self.expense_listbox.insert(
                tk.END, f"{expense} - {item} - {category} ({date})"
            )
            self.expense_entry.delete(0, tk.END)
            self.item_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Expense and Date cannot be empty.")
        self.update_total_label()

    def edit_expense(self):
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_expense = self.expenses[selected_index]
            new_expense = simpledialog.askstring(
                "Edit Expense", "Enter new expense:", initialvalue=selected_expense[0]
            )
            if new_expense:
                self.expenses[selected_index] = (
                    new_expense,
                    selected_expense[1],
                    selected_expense[2],
                    selected_expense[3],
                )
                self.refresh_list()
                self.update_total_label()

    def delete_expense(self):
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            del self.expenses[selected_index]
            self.expense_listbox.delete(selected_index)
            self.update_total_label()

    def refresh_list(self):
        self.expense_listbox.delete(0, tk.END)
        for expense, item, category, date in self.expenses:
            self.expense_listbox.insert(
                tk.END, f"{expense} - {item} - {category} ({date})"
            )

    def update_total_label(self):
        today_date = datetime.now().strftime("%Y-%m-%d")

        with open("expenses.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            csv_expenses = [expense for expense in reader if expense[3] == today_date]

        all_expenses = self.expenses + csv_expenses

        total_expenses = sum(float(expense[0]) for expense in all_expenses)

        self.total_label.config(text=f"Today's Expenses ({today_date}): Rs : {total_expenses:.2f}")

        total_expenses_all_day = sum(float(expense[0]) for expense in all_expenses if expense[3] <= today_date)

        self.total_label_all_day.config(text=f"Total Expenses All Day ({today_date}): Rs :{total_expenses_all_day:.2f}")

    def save_expenses(self):
        with open("expenses.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for expense in self.expenses:
                writer.writerow(expense)

    def show_expenses_chart(self):
        category_totals = defaultdict(float)
        daily_totals = defaultdict(float)

        with open("expenses.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                try:
                    amount = float(row[0])
                    category = row[2]
                    date = row[3]
                except ValueError:
                    continue
                category_totals[category] += amount
                daily_totals[date] += amount

        categories = list(category_totals.keys())
        expenses = list(category_totals.values())

        # Plot the pie chart
        plt.figure(figsize=(18, 6))
        plt.subplot(1, 2, 1)
        plt.pie(
            expenses, labels=categories, autopct="%1.1f%%", startangle=140, shadow=True
        )
        plt.axis("equal")
        plt.title(f"Expense Categories Distribution (Rs )")

        dates = list(daily_totals.keys())
        daily_expenses = list(daily_totals.values())

        plt.subplot(1, 2, 2)
        x = np.arange(len(dates))
        plt.bar(x, daily_expenses, align='center')
        plt.xticks(x, dates)
        plt.xlabel('Date')
        plt.ylabel('Expenses (Rs)')
        plt.title('Daily Expense Bar Graph')

        plt.show()

    def calculate_total_monthly_expenses(self):
        monthly_totals = {}

        with open("expenses.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  
            for row in reader:
                try:
                    amount = float(row[0])
                    date = row[3]
                except ValueError:
                    continue
                year_month = date[:7]
                monthly_totals[year_month] = monthly_totals.get(year_month, 0) + amount

        # Calculate the total monthly expenses
        total_monthly_expenses = sum(monthly_totals.values())
        messagebox.showinfo("Monthly Expenses", f"Total Expenses: Rs {total_monthly_expenses:.2f}")

    def set_today_date(self, event):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
