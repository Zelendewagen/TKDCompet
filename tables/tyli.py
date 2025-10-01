import os
import sqlite3
from datetime import datetime
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter.filedialog import askopenfilename

import pandas as pd

import config
from config import DB_FILE


class TyliFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.current_id = None
        self.category_table = None
        self.unallocated_table = None
        self.athletes_table = None

        self.create_top_buttons()
        self.create_category_table()
        self.create_unallocated_table()
        self.create_athletes_table()

    def create_top_buttons(self):
        buttons_frame = tk.Frame(self)
        back_button = ttk.Button(buttons_frame, text="\u2190", command=self.back, width=10)
        add_category = ttk.Button(buttons_frame, text="Добавить категорию",
                                  command=self.open_add_change_category_window, width=20)

        back_button.pack(side="left", padx=5, pady=5)
        add_category.pack(side="left", padx=5, pady=5)

        buttons_frame.pack(fill="both", padx=5, pady=(10, 0))

    def create_category_table(self):
        self.category_table = self.create_table(
            label_text="Параметры",
            headers=['№', 'Пол', 'Возраст от', 'До', 'Категория от', 'До '])

    def create_unallocated_table(self):
        self.unallocated_table = self.create_table(
            label_text="Не распределенные",
            headers=['№', 'ФИО', 'Полных лет', 'Категория', 'Город', 'Тренер', 'Положение', 'ID'])

    def create_athletes_table(self):
        self.athletes_table = self.create_table(
            label_text="Участники",
            headers=['№', 'ФИО', 'Полных лет', 'Категория', 'Город', 'Тренер', 'Положение', 'ID'])

    def create_table(self, label_text, headers):
        frame = tk.Frame(self, bd=1, relief="sunken")
        frame.pack(side="left", fill="both", padx=(10, 0), pady=10, expand=True)
        label = tk.Label(frame, text=label_text, font=("Arial", 14))
        label.pack(side="top", pady=(5, 2))

        table = ttk.Treeview(frame, columns=headers, show='headings')

        total_width = frame.winfo_reqwidth() or 300
        col_width = total_width // len(headers)
        for header in headers:
            table.heading(header, text=header)
            table.column(header, width=col_width, anchor='center')

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscroll=scrollbar.set)

        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # table.bind('<Button-3>', self.right_button_menu)
        # table.bind("<Double-1>", self.on_double_click)

        return table

    def open_add_change_category_window(self, change=False, compet_id=None):
        self.top_window = tk.Toplevel()
        self.top_window.grab_set()
        title = 'Изменить параметры' if change else 'Добавить параметры'
        self.top_window.title(title)
        self.top_window.geometry(config.geometry(self.master, config.tyli_window_width, config.tyli_window_height))
        self.top_window.resizable(False, False)
        self.top_window.transient(self)

        frame = tk.Frame(self.top_window)
        frame.pack(fill="both", padx=10, pady=10, expand=True)
        frame.columnconfigure(index=1, weight=1)
        frame.columnconfigure(index=3, weight=1)

        ages = [str(i) for i in range(1, 100)]
        entries = [ttk.Combobox(frame, values=ages, state="readonly", width=30) for _ in range(5)]
        entries.insert(0, ttk.Combobox(frame, values=['мужской', 'женский'], state="readonly"))

        tk.Label(frame, text="Пол:").grid(row=0, column=0, sticky="w", pady=(0, 10))
        entries[0].grid(row=0, column=1, columnspan=3, sticky="ew", pady=(0, 10))

        tk.Label(frame, text="Возраст от:").grid(row=1, column=0, sticky="w", pady=(0, 10))
        tk.Label(frame, text="до:").grid(row=1, column=2, sticky="w", pady=(0, 10), padx=(10, 0))
        entries[1].grid(row=1, column=1, sticky="w", pady=(0, 10))
        entries[1].bind("<<ComboboxSelected>>", lambda x: self.update_values(entries[1], entries[2]))
        entries[2].grid(row=1, column=3, sticky="w", pady=(0, 10))

        tk.Label(frame, text="Категория от:").grid(row=2, column=0, sticky="w")
        tk.Label(frame, text="до:").grid(row=2, column=2, sticky="w", padx=(10, 0))
        entries[3].grid(row=2, column=1, sticky="w")
        entries[3].bind("<<ComboboxSelected>>", lambda x: self.update_values(entries[3], entries[4]))
        entries[4].grid(row=2, column=3, sticky="w")

        buttons_frame = tk.Frame(frame)
        buttons_frame.grid(columnspan=4, row=3, pady=20, sticky="ew")

        if change:
            conn = sqlite3.connect(config.DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tyli WHERE competition_id =?", (compet_id,))
            values = cursor.fetchone()
            conn.close()
            print(values)
            for i, entry in enumerate(entries):
                entries[i].insert(0, values[i + 2])

            change_button = ttk.Button(buttons_frame, text='Изменить', width=15,
                                       command=lambda:
                                       self.add_change_category(entries, cat_id=values[0], change=True))
            change_button.pack(fill="both", expand=True, side="left", padx=5)
        else:
            add_button = ttk.Button(buttons_frame, text='Добавить', width=15,
                                    command=lambda: self.add_change_category(entries))
            add_button.pack(fill="both", expand=True, side="left", padx=5)

        cancel_button2 = ttk.Button(buttons_frame, text="Отмена", command=self.top_window.destroy, width=15)
        cancel_button2.pack(fill="both", expand=True, side="left", padx=5)

    def back(self):
        self.master.show_table('спортсмены', self)

    def add_change_category(self, entries, cat_id=None, change=False):
        pass

    def update_values(self, entry_from, entry_to):
        entry_to['values'] = [str(i) for i in range(int(entry_from.get()), 100)]
        if entry_to.get() and int(entry_to.get()) < int(entry_from.get()):
            entry_to.set('')
