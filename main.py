import tkinter as tk
from tkinter import messagebox, ttk
import os
import sqlite3

from tables.athletes import AthletesFrame
from tables.competitions import CompetitionsFrame

DB_FILE = "data.db"
DB_FOLDER = "."


def check_database():
    db_path = os.path.join(DB_FOLDER, DB_FILE)
    if os.path.exists(db_path):
        for row in competitions_frame.table.get_children():
            competitions_frame.table.delete(row)
    else:
        messagebox.showwarning("TKD", f"Нету базы: {db_path}")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS competitions (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             name TEXT NOT NULL,
    #             date TEXT,
    #             location TEXT,
    #             club TEXT,
    #             main_judge TEXT,
    #             judge TEXT,
    #             secretary TEXT
    #         )
    #         """)
    #
    # cursor.execute(
    #     "INSERT INTO competitions (name, date, location, club, main_judge, judge, secretary) VALUES (?, ?, ?, ?, ?, ?, ?)",
    #     ("Первенство и фестиваль", "22-23 ноября", "г. Находка", "клуб1", "Ким А Т", "Ким А Т", "Ким К А"))
    # cursor.execute(
    #     "INSERT INTO competitions (name, date, location, club, main_judge, judge, secretary) VALUES (?, ?, ?, ?, ?, ?, ?)",
    #     ("Соревнование во владивостоке", "24-25 ноября", "г. Владивосток", "клуб2", "Ким А Т", "Ким А Т", "Ким К А"))
    # conn.commit()

    cursor.execute("SELECT * FROM competitions")
    competitions = cursor.fetchall()
    conn.close()

    for row in competitions:
        compet_frame.table.insert("", tk.END, values=(row[0], row[2], row[3], row[1], row[4]))


#######################################################################################################################
root = tk.Tk()
root.title("TKD")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.55)
window_height = int(screen_height * 0.45)
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.option_add("*tearOff", tk.FALSE)
#######################################################################################################################
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                borderwidth=1,
                relief="solid")
# print(style.theme_names())
#######################################################################################################################
main = tk.Frame(root)
main.pack(fill="both", expand=True)

check_button = tk.Button(main, text="Загрузить", command=check_database, font=("Arial", 16))
check_button.pack(pady=10)

competitions_frame = CompetitionsFrame(main)
competitions_frame.pack(fill="both", expand=True)
athletes_frame = AthletesFrame(main)
#######################################################################################################################
root.mainloop()
