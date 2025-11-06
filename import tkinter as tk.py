import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# ------------------ DATABASE CONNECTION ------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # your MySQL username
        password="Aayush@#72",          # your MySQL password
        database="inventory_db"
    )

# ------------------ FUNCTIONS ------------------
def add_product():
    name = entry_name.get()
    price = entry_price.get()
    qty = entry_qty.get()
    reorder = entry_reorder.get()

    if name == "" or price == "" or qty == "":
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO products (name, price, quantity, reorder_level) VALUES (%s,%s,%s,%s)",
                   (name, price, qty, reorder))
    db.commit()
    db.close()

    messagebox.showinfo("Success", "Product added successfully!")
    clear_fields()
    view_products()

def view_products():
    for row in tree.get_children():
        tree.delete(row)
    
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    for r in rows:
        tree.insert("", tk.END, values=r)
    db.close()

def sell_product():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a product to sell!")
        return
    
    data = tree.item(selected, "values")
    pid, name, price, qty, reorder = data

    if int(qty) <= 0:
        messagebox.showerror("Error", f"{name} is out of stock!")
        return
    
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE products SET quantity = quantity - 1 WHERE id = %s", (pid,))
    db.commit()
    db.close()

    messagebox.showinfo("Sale Recorded", f"Sold 1 unit of {name}")
    view_products()

    if int(qty) - 1 < int(reorder):
        messagebox.showwarning("Low Stock", f"⚠️ Low stock alert for {name}!")

def purchase_product():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a product to purchase more!")
        return
    
    data = tree.item(selected, "values")
    pid = data[0]
    
    amount = tk.simpledialog.askinteger("Purchase", "Enter quantity to add:")
    if amount is None or amount <= 0:
        return
    
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE products SET quantity = quantity + %s WHERE id = %s", (amount, pid))
    db.commit()
    db.close()

    messagebox.showinfo("Success", "Stock updated successfully!")
    view_products()

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_qty.delete(0, tk.END)
    entry_reorder.delete(0, tk.END)

# ------------------ UI SETUP ------------------
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("750x500")
root.configure(bg="#ecf0f1")

title = tk.Label(root, text="Inventory Management System", font=("Arial", 18, "bold"), bg="#3498db", fg="white")
title.pack(fill=tk.X, pady=10)

frame = tk.Frame(root, bg="white")
frame.pack(pady=10)

tk.Label(frame, text="Product Name:", bg="white").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Price:", bg="white").grid(row=1, column=0, padx=10, pady=5)
entry_price = tk.Entry(frame)
entry_price.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame, text="Quantity:", bg="white").grid(row=2, column=0, padx=10, pady=5)
entry_qty = tk.Entry(frame)
entry_qty.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame, text="Reorder Level:", bg="white").grid(row=3, column=0, padx=10, pady=5)
entry_reorder = tk.Entry(frame)
entry_reorder.grid(row=3, column=1, padx=10, pady=5)

tk.Button(frame, text="Add Product", command=add_product, bg="#2ecc71", fg="white").grid(row=4, column=0, pady=10)
tk.Button(frame, text="View Products", command=view_products, bg="#3498db", fg="white").grid(row=4, column=1, pady=10)

# TreeView (Product Table)
cols = ("ID", "Name", "Price", "Quantity", "Reorder Level")
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="#ecf0f1")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Sell Product", command=sell_product, bg="#e74c3c", fg="white", width=15).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Purchase Product", command=purchase_product, bg="#f1c40f", fg="white", width=15).grid(row=0, column=1, padx=10)

view_products()
root.mainloop()
