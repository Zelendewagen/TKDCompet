import tkinter as tk
from tkinter import messagebox, ttk
import os
import sqlite3

DB_FILE = "data.db"
DB_FOLDER = "."
competitions = []


def check_database():
    global competitions
    db_path = os.path.join(DB_FOLDER, DB_FILE)
    if os.path.exists(db_path):
        messagebox.showinfo("TKD", f"Загружено")
    else:
        messagebox.showwarning("TKD", f"Новая база: {db_path}")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS competitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT,
                location TEXT,
                club TEXT,
                main_judge TEXT,
                judge TEXT,
                secretary TEXT
            )
            """)

    cursor.execute(
        "INSERT INTO competitions (name, date, location, club, main_judge, judge, secretary) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("Первенство и фестиваль", "22-23 ноября", "г. Находка", "клуб", "Ким А Т", "Ким А Т", "Ким К А"))
    cursor.execute(
        "INSERT INTO competitions (name, date, location, club, main_judge, judge, secretary) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("Первенство и фестиваль", "24-25 ноября", "г. Находка", "клуб", "Ким А Т", "Ким А Т", "Ким К А"))
    conn.commit()

    cursor.execute("SELECT * FROM competitions")
    competitions = cursor.fetchall()
    conn.close()

    for row in competitions:
        compet_table.insert("", tk.END, values=row)


def right_button_menu(event):
    item = compet_table.identify_row(event.y)
    if item:
        compet_table.selection_set(item)
        compet_table.focus(item)

    popup_menu = tk.Menu(root)
    event.widget.focus()
    file_menu = tk.Menu(popup_menu)
    file_menu.add_command(label='Изменить',command=lambda: print(compet_table.item(item).get('values')))
    file_menu.add_separator()
    file_menu.add_command(label='Удалить')
    file_menu.post(event.x_root, event.y_root)

def on_double_click(event):
    item = compet_table.identify_row(event.y)
    if item:
        values = compet_table.item(item, "values")
        print(values)

#######################################################################################################################
root = tk.Tk()
root.title("TKD")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.35)
window_height = int(screen_height * 0.45)
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.option_add("*tearOff", tk.FALSE)
#######################################################################################################################
exit_button = tk.Button(root, text="Выход", command=root.destroy, font=("Arial", 20))
exit_button.pack(pady=10)
check_button = tk.Button(root, text="Загрузить БД", command=check_database, font=("Arial", 16))
check_button.pack()
#######################################################################################################################
style = ttk.Style()
style.configure("Treeview",
                borderwidth=1,
                relief="solid")
#######################################################################################################################
heads = ['Дата', 'Место проведения', 'Название соревнования']
compet_table = ttk.Treeview(root, columns=heads, show='headings', selectmode="browse")
for header in heads:
    compet_table.heading(header, text=header, anchor='w')
compet_table.column('Дата', minwidth=30, width=30)
compet_table.column('Место проведения', stretch=True, width=110, minwidth=100)
compet_table.column('Название соревнования', stretch=True, width=150, minwidth=110)
compet_table.pack(side="left", fill="both", padx=10, pady=10, expand=True)
compet_table.bind('<Button-3>', right_button_menu)
compet_table.bind("<Double-1>", on_double_click)
#######################################################################################################################
scrollbar = ttk.Scrollbar(root, orient="vertical", command=compet_table.yview)
compet_table.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y", pady=20)
#######################################################################################################################
root.mainloop()
