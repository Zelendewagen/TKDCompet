import tkinter as tk
from tkinter import messagebox, ttk
import os
import sqlite3

import config
from config import DB_FOLDER, DB_FILE
from tables.athletes import AthletesFrame
from tables.competitions import CompetitionsFrame
from tables.massogi import MassogiFrame
from tables.tyli import TyliFrame


class MainFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.test = 12345
        self.competitions_frame = CompetitionsFrame(self)
        self.athletes_frame = AthletesFrame(self)
        self.tyli_frame = TyliFrame(self)
        self.massogi_frame = MassogiFrame(self)
        self.competitions_frame.pack(fill="both", padx=10, pady=10, expand=True)
        self.check_database()

    def check_database(self):
        db_path = os.path.join(DB_FOLDER, DB_FILE)
        if os.path.exists(db_path):
            self.create_db()
            self.competitions_frame.update_table()
        else:
            messagebox.showwarning("TKD", f"Новая база данных: {db_path}")
            self.create_db()

    @staticmethod
    def create_db():
        with sqlite3.connect(DB_FILE) as conn:
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
                                    secretary TEXT)
                                """)

            cursor.execute("""
                                CREATE TABLE IF NOT EXISTS athletes (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    competition_id INTEGER,
                                    name TEXT NOT NULL,
                                    gender TEXT,
                                    date TEXT,
                                    age INTEGER,
                                    weight INTEGER,
                                    category INTEGER,
                                    location TEXT,
                                    club TEXT,
                                    trainer TEXT,
                                    tyli TEXT,
                                    massogi TEXT,
                                    FOREIGN KEY (competition_id) REFERENCES competitions (id))
                        """)

            cursor.execute("""
                                CREATE TABLE IF NOT EXISTS tyli (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    competition_id INTEGER,
                                    gender TEXT,
                                    age_form INTEGER,
                                    age_to INTEGER,
                                    category_from INTEGER,
                                    category_to INTEGER,
                                    users TEXT,
                                    FOREIGN KEY (competition_id) REFERENCES competitions (id))
                                """)

            cursor.execute("""
                                CREATE TABLE IF NOT EXISTS massogi (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    competition_id INTEGER,
                                    gender TEXT,
                                    age_form INTEGER,
                                    age_to INTEGER,
                                    category_from INTEGER,
                                    category_to INTEGER,
                                    weight_from INTEGER,
                                    weight_to INTEGER,
                                    users TEXT,
                                    FOREIGN KEY (competition_id) REFERENCES competitions (id))
                                """)

            conn.commit()

    def show_table(self, name, frame):
        names = {'соревнования': self.competitions_frame, 'спортсмены': self.athletes_frame,
                 'тыли': self.tyli_frame, 'массоги': self.massogi_frame}
        frame.pack_forget()
        names[name].pack(fill="both", padx=10, pady=10, expand=True)


#######################################################################################################################
root = tk.Tk()
root.title("TKD competitions manager")
root.geometry(config.geometry(root, config.main_width, config.main_height))
root.option_add("*tearOff", tk.FALSE)
root.iconbitmap("icons/tkd.ico")
#######################################################################################################################
style = ttk.Style()
style.theme_use("vista")
style.configure("Treeview",
                borderwidth=1,
                relief="solid")
# print(style.theme_names())
#######################################################################################################################
main = MainFrame(root)
main.pack(fill="both", expand=True)
#######################################################################################################################
root.mainloop()
