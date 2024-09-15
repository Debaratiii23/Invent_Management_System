import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import datetime

# User credentials for basic authentication
users = {
    "Debarati": "2312",
    "user1": "pass1",
}

# CSV file to store inventory and sales data
inventory_file = 'inventory.csv'
sales_file = 'sales.csv'
users_file = 'users.csv'

# Function to create the inventory and sales files if they don't exist
def create_files():
    if not os.path.exists(inventory_file):
        with open(inventory_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Product Name", "Quantity", "Price"])
            # Pre-adding 10 products to the inventory
            products = [
                ["pro001", "Laptop", "50", "80000"],
                ["pro002", "Smartphone", "100", "50000"],
                ["pro003", "Headphones", "200", "3000"],
                ["pro004", "Mouse", "150", "2000"],
                ["pro005", "Keyboard", "100", "2500"],
                ["pro006", "Monitor", "75", "15000"],
                ["pro007", "Tablet", "80", "30000"],
                ["pro008", "Printer", "30", "10000"],
                ["pro009", "Camera", "40", "40000"],
                ["pro010", "Speakers", "60", "5000"]
            ]
            writer.writerows(products)

    if not os.path.exists(sales_file):
        with open(sales_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Product ID", "Product Name", "Quantity Sold", "Date"])

    if not os.path.exists(users_file):
        with open(users_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Password"])
            for user, password in users.items():
                writer.writerow([user, password])

# Function to load inventory data from CSV
def load_inventory():
    inventory = []
    with open(inventory_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            inventory.append(row)
    return inventory

# Function to add a product to the inventory
def add_product(product_id, name, quantity, price):
    with open(inventory_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([product_id, name, quantity, price])

# Function to update the inventory after edit/delete
def update_inventory(inventory):
    with open(inventory_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Product Name", "Quantity", "Price"])
        for product in inventory:
            writer.writerow([product["ID"], product["Product Name"], product["Quantity"], product["Price"]])

# Function to check if the stock is low
def check_low_stock():
    low_stock_items = []
    inventory = load_inventory()
    for product in inventory:
        if int(product["Quantity"]) < 100:
            low_stock_items.append(product)
    return low_stock_items

# Function to authenticate users
def authenticate(username, password):
    with open(users_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Username"] == username and row["Password"] == password:
                return True
    return False

# Function to manage sales data
def record_sale(product_id, quantity_sold):
    product = get_product_by_id(product_id)
    if product:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        with open(sales_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([product_id, product['Product Name'], quantity_sold, current_date])

# Function to get a product by ID
def get_product_by_id(product_id):
    inventory = load_inventory()
    for product in inventory:
        if product["ID"] == product_id:
            return product
    return None

# Function to load sales data
def load_sales():
    sales = []
    with open(sales_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sales.append(row)
    return sales

# Function to filter sales by date (for daily, monthly, yearly summary)
def filter_sales_by_date(sales, date_format):
    filtered_sales = []
    current_date = datetime.datetime.now().strftime(date_format)
    for sale in sales:
        if sale["Date"].startswith(current_date):
            filtered_sales.append(sale)
    return filtered_sales

# GUI Functionality
def login():
    def verify_login():
        username = username_entry.get()
        password = password_entry.get()

        if authenticate(username, password):
            messagebox.showinfo("Success", "Login Successful!")
            login_window.destroy()
            inventory_management()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    login_window = tk.Tk()
    login_window.title("Inventory Management - Login")

    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Login", command=verify_login).pack()

    login_window.mainloop()

def inventory_management():
    inventory_window = tk.Tk()
    inventory_window.title("Inventory Management System")

    # Function to refresh the inventory view
    def refresh_inventory():
        for item in inventory_tree.get_children():
            inventory_tree.delete(item)
        inventory = load_inventory()
        for product in inventory:
            inventory_tree.insert('', tk.END, values=(product["ID"], product["Product Name"], product["Quantity"], product["Price"]))

    # Function to add product
    def add_product_popup():
        def save_product():
            product_id = product_id_entry.get()
            product_name = product_name_entry.get()
            product_quantity = quantity_entry.get()
            product_price = price_entry.get()

            if not product_id or not product_name or not product_quantity.isdigit() or not product_price.isdigit():
                messagebox.showerror("Error", "Invalid input! Ensure all fields are correctly filled.")
            else:
                add_product(product_id, product_name, product_quantity, product_price)
                refresh_inventory()
                add_window.destroy()

        add_window = tk.Toplevel(inventory_window)
        add_window.title("Add Product")

        tk.Label(add_window, text="Product ID:").pack()
        product_id_entry = tk.Entry(add_window)
        product_id_entry.pack()

        tk.Label(add_window, text="Product Name:").pack()
        product_name_entry = tk.Entry(add_window)
        product_name_entry.pack()

        tk.Label(add_window, text="Quantity:").pack()
        quantity_entry = tk.Entry(add_window)
        quantity_entry.pack()

        tk.Label(add_window, text="Price:").pack()
        price_entry = tk.Entry(add_window)
        price_entry.pack()

        tk.Button(add_window, text="Save", command=save_product).pack()

    # Function to edit a product
    def edit_product_popup():
        def save_edited_product():
            product_id = product_id_entry.get()
            product_name = product_name_entry.get()
            product_quantity = quantity_entry.get()
            product_price = price_entry.get()

            inventory = load_inventory()
            for product in inventory:
                if product["ID"] == product_id:
                    product["Product Name"] = product_name
                    product["Quantity"] = product_quantity
                    product["Price"] = product_price
                    update_inventory(inventory)
                    refresh_inventory()
                    edit_window.destroy()
                    return
            messagebox.showerror("Error", "Product not found!")

        edit_window = tk.Toplevel(inventory_window)
        edit_window.title("Edit Product")

        tk.Label(edit_window, text="Product ID:").pack()
        product_id_entry = tk.Entry(edit_window)
        product_id_entry.pack()

        tk.Label(edit_window, text="Product Name:").pack()
        product_name_entry = tk.Entry(edit_window)
        product_name_entry.pack()

        tk.Label(edit_window, text="Quantity:").pack()
        quantity_entry = tk.Entry(edit_window)
        quantity_entry.pack()

        tk.Label(edit_window, text="Price:").pack()
        price_entry = tk.Entry(edit_window)
        price_entry.pack()

        tk.Button(edit_window, text="Save Changes", command=save_edited_product).pack()

    # Function to delete a product by ID
    def delete_product_by_id():
        product_id = delete_product_entry.get()
        inventory = load_inventory()
        inventory = [product for product in inventory if product["ID"] != product_id]
        update_inventory(inventory)
        refresh_inventory()

    # Function to show low stock alert
    def low_stock_alert():
        low_stock_items = check_low_stock()
        if low_stock_items:
            alert = "\n".join([f'{prod["Product Name"]}: {prod["Quantity"]} left' for prod in low_stock_items])
            messagebox.showwarning("Low Stock Alert", f"These items are low on stock:\n\n{alert}")
        else:
            messagebox.showinfo("Low Stock Alert", "All items have sufficient stock.")

    # Function to show general sales summary
    def show_general_sales_summary():
        sales = load_sales()
        summary = ""
        if sales:
            for sale in sales:
                summary += f'Product: {sale["Product Name"]}, Quantity Sold: {sale["Quantity Sold"]}, Date: {sale["Date"]}\n'
            messagebox.showinfo("General Sales Summary", summary)
        else:
            messagebox.showinfo("General Sales Summary", "No sales recorded.")

    # Function to show daily sales summary
    def show_daily_sales_summary():
        sales = load_sales()
        daily_sales = filter_sales_by_date(sales, "%Y-%m-%d")
        summary = ""
        if daily_sales:
            for sale in daily_sales:
                summary += f'Product: {sale["Product Name"]}, Quantity Sold: {sale["Quantity Sold"]}, Date: {sale["Date"]}\n'
            messagebox.showinfo("Daily Sales Summary", summary)
        else:
            messagebox.showinfo("Daily Sales Summary", "No sales recorded today.")

    # Function to show monthly sales summary
    def show_monthly_sales_summary():
        sales = load_sales()
        monthly_sales = filter_sales_by_date(sales, "%Y-%m")
        summary = ""
        if monthly_sales:
            for sale in monthly_sales:
                summary += f'Product: {sale["Product Name"]}, Quantity Sold: {sale["Quantity Sold"]}, Date: {sale["Date"]}\n'
            messagebox.showinfo("Monthly Sales Summary", summary)
        else:
            messagebox.showinfo("Monthly Sales Summary", "No sales recorded this month.")

    # Function to show yearly sales summary
    def show_yearly_sales_summary():
        sales = load_sales()
        yearly_sales = filter_sales_by_date(sales, "%Y")
        summary = ""
        if yearly_sales:
            for sale in yearly_sales:
                summary += f'Product: {sale["Product Name"]}, Quantity Sold: {sale["Quantity Sold"]}, Date: {sale["Date"]}\n'
            messagebox.showinfo("Yearly Sales Summary", summary)
        else:
            messagebox.showinfo("Yearly Sales Summary", "No sales recorded this year.")

    # Inventory management UI
    inventory_tree = ttk.Treeview(inventory_window, columns=("ID", "Product Name", "Quantity", "Price"), show="headings")
    inventory_tree.heading("ID", text="ID")
    inventory_tree.heading("Product Name", text="Product Name")
    inventory_tree.heading("Quantity", text="Quantity")
    inventory_tree.heading("Price", text="Price")
    inventory_tree.pack()

    refresh_inventory()

    # Buttons for adding, editing, deleting products
    tk.Button(inventory_window, text="Add Product", command=add_product_popup).pack()
    tk.Button(inventory_window, text="Edit Product", command=edit_product_popup).pack()

    tk.Label(inventory_window, text="Enter Product ID to Delete:").pack()
    delete_product_entry = tk.Entry(inventory_window)
    delete_product_entry.pack()
    tk.Button(inventory_window, text="Delete Product", command=delete_product_by_id).pack()

    # Buttons for sales summaries
    tk.Button(inventory_window, text="General Sales Summary", command=show_general_sales_summary).pack()
    tk.Button(inventory_window, text="Daily Sales Summary", command=show_daily_sales_summary).pack()
    tk.Button(inventory_window, text="Monthly Sales Summary", command=show_monthly_sales_summary).pack()
    tk.Button(inventory_window, text="Yearly Sales Summary", command=show_yearly_sales_summary).pack()

    # Button for low stock alert
    tk.Button(inventory_window, text="Low Stock Alert", command=low_stock_alert).pack()

    inventory_window.mainloop()

# Start the program by creating necessary files and opening login window
create_files()
login()
