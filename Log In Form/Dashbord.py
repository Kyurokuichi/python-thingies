import tkinter as tk
from tkinter import messagebox, simpledialog

# Sample data for the menu and users
menus = {"Burger": 5.0, "Pizza": 8.0, "Pasta": 6.5}
users = {"admin": {"password": "admin123", "role": "admin"}, "staff": {"password": "staff123", "role": "staff"}}
orders = []


# Function to calculate the total amount for the order
def calculate_total():
    total = sum(item['price'] for item in orders)
    total_label.config(text=f"Total: ${total:.2f}")
    return total


# Function to print the receipt
def print_receipt():
    receipt_text = "Receipt:\n"
    for item in orders:
        receipt_text += f"{item['name']} - ${item['price']:.2f}\n"
    receipt_text += f"\nTotal: ${calculate_total():.2f}"
    messagebox.showinfo("Receipt", receipt_text)


# Function to add an item to the order
def add_item_to_order():
    item_name = menu_var.get()
    if item_name:
        price = menus.get(item_name, 0)
        orders.append({"name": item_name, "price": price})
        order_listbox.insert(tk.END, f"{item_name} - ${price:.2f}")
        calculate_total()


# Function to void an item from the order
def void_item():
    selected_item_index = order_listbox.curselection()
    if selected_item_index:
        item_name = order_listbox.get(selected_item_index[0]).split(' - ')[0]
        orders[:] = [item for item in orders if item['name'] != item_name]
        order_listbox.delete(selected_item_index)
        calculate_total()


# Staff Dashboard
def staff_dashboard():
    global menu_var, order_listbox, total_label
    staff_window = tk.Toplevel()
    staff_window.title("Staff Dashboard")

    # Menu selection
    menu_label = tk.Label(staff_window, text="Select a Menu Item")
    menu_label.pack()
    menu_var = tk.StringVar(value="Burger")  # Default value
    menu_menu = tk.OptionMenu(staff_window, menu_var, *menus.keys())
    menu_menu.pack()

    # Add and Void buttons
    add_button = tk.Button(staff_window, text="Add to Order", command=add_item_to_order)
    add_button.pack()

    void_button = tk.Button(staff_window, text="Void Item", command=void_item)
    void_button.pack()

    # Order listbox and total label
    order_listbox = tk.Listbox(staff_window)
    order_listbox.pack()

    total_label = tk.Label(staff_window, text="Total: $0.00")
    total_label.pack()

    receipt_button = tk.Button(staff_window, text="Print Receipt", command=print_receipt)
    receipt_button.pack()


# Admin Dashboard
def admin_dashboard():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Dashboard")

    # Add menu item functionality
    def add_menu_item():
        item_name = simpledialog.askstring("Menu Item", "Enter menu item name:")
        item_price = simpledialog.askfloat("Price", "Enter price:")
        if item_name and item_price:
            menus[item_name] = item_price
            messagebox.showinfo("Success", f"{item_name} added with price ${item_price:.2f}")
            refresh_menu()

    # Edit menu price functionality
    def edit_price():
        item_name = simpledialog.askstring("Menu Item", "Enter menu item name to edit price:")
        if item_name in menus:
            new_price = simpledialog.askfloat("Price", "Enter new price:")
            if new_price is not None:
                menus[item_name] = new_price
                messagebox.showinfo("Success", f"Price of {item_name} updated to ${new_price:.2f}")
                refresh_menu()
        else:
            messagebox.showerror("Error", "Menu item not found")

    # Edit user information functionality
    def edit_user_info():
        username = simpledialog.askstring("Username", "Enter username to edit info:")
        if username in users:
            new_password = simpledialog.askstring("Password", "Enter new password:")
            users[username]["password"] = new_password
            messagebox.showinfo("Success", f"Password for {username} updated.")
        else:
            messagebox.showerror("Error", "User not found")

    # Add user functionality
    def add_user():
        username = simpledialog.askstring("Username", "Enter new username:")
        if username not in users:
            password = simpledialog.askstring("pass", "Enter password:")
            role = simpledialog.askstring("Role", "Enter role (admin or staff):")
            users[username] = {"password": password, "role": role}
            messagebox.showinfo("Success", f"User {username} added as {role}.")
        else:
            messagebox.showerror("Error", "Username already exists")

    # Refresh the menu in the admin dashboard
    def refresh_menu():
        menu_listbox.delete(0, tk.END)
        for item, price in menus.items():
            menu_listbox.insert(tk.END, f"{item} - ${price:.2f}")

    # Menu listbox to display current menu items
    menu_listbox = tk.Listbox(admin_window)
    menu_listbox.pack()

    # Add, Edit, and Refresh menu buttons
    add_menu_button = tk.Button(admin_window, text="Add Menu Item", command=add_menu_item)
    add_menu_button.pack()

    edit_price_button = tk.Button(admin_window, text="Edit Price", command=edit_price)
    edit_price_button.pack()

    add_user_button = tk.Button(admin_window, text="Add User", command=add_user)
    add_user_button.pack()

    edit_user_button = tk.Button(admin_window, text="Edit User Info", command=edit_user_info)
    edit_user_button.pack()

    refresh_button = tk.Button(admin_window, text="Refresh Menu", command=refresh_menu)
    refresh_button.pack()


# Main login window
def login():
    def on_login():
        username = username_entry.get()
        password = password_entry.get()

        if username in users and users[username]["password"] == password:
            if users[username]["role"] == "admin":
                admin_dashboard()
            else:
                staff_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_window = tk.Tk()
    login_window.title("Login")

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()

    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()

    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    login_button = tk.Button(login_window, text="Login", command=on_login)
    login_button.pack()

    login_window.mainloop()


# Run the application
login()
