import tkinter as tk
from tkinter import messagebox, ttk
import os
import sqlite3

from config import DB_FOLDER, DB_FILE
from tables.athletes import AthletesFrame
from tables.competitions import CompetitionsFrame




def check_database():
    db_path = os.path.join(DB_FOLDER, DB_FILE)
    if os.path.exists(db_path):
        load_competitions_table()
    else:
        messagebox.showwarning("TKD", f"Новая база данных: {db_path}")
        create_db()


def load_competitions_table():
    for row in competitions_frame.table.get_children():
        competitions_frame.table.delete(row)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM competitions")
    competitions = cursor.fetchall()
    conn.close()
    for row in competitions:
        competitions_frame.table.insert("", tk.END, values=(row[0], row[2], row[3], row[1], row[4]))


def create_db():
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

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS athletes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competition_id INTEGER,
                name TEXT NOT NULL,
                gender TEXT,
                date TEXT,
                age TEXT,
                weight TEXT,
                category TEXT,
                region TEXT,
                trainer TEXT,
                massogi TEXT,
                tyli TEXT,
                FOREIGN KEY (competition_id) REFERENCES competitions (id))
            """)

    conn.commit()
    conn.close()


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

competitions_frame = CompetitionsFrame(main)
competitions_frame.pack(fill="both", expand=True)
athletes_frame = AthletesFrame(main)
check_database()
#######################################################################################################################
root.mainloop()
