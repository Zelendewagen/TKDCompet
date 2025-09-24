import tkinter as tk
from tkinter import messagebox, ttk
import os
import sqlite3

import config
from config import DB_FOLDER, DB_FILE
from tables.athletes import AthletesFrame
from tables.competitions import CompetitionsFrame


def check_database():
    db_path = os.path.join(DB_FOLDER, DB_FILE)
    if os.path.exists(db_path):
        competitions_frame.update_table()
    else:
        messagebox.showwarning("TKD", f"Новая база данных: {db_path}")
        create_db()


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
root.title("TKD competitions manager")
root.geometry(config.geometry(root, config.main_width, config.main_height))
root.option_add("*tearOff", tk.FALSE)
#######################################################################################################################
style = ttk.Style()
style.theme_use("vista")
style.configure("Treeview",
                borderwidth=1,
                relief="solid")
print(style.theme_names())
#######################################################################################################################
main = tk.Frame(root)
main.pack(fill="both", expand=True)

competitions_frame = CompetitionsFrame(main)
competitions_frame.pack(fill="both", expand=True)

athletes_frame = AthletesFrame(main)
check_database()
#######################################################################################################################
root.mainloop()
