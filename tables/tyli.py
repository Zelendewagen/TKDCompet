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

        self.categories = [f"{i} гып" for i in range(10, 0, -1)] + [f"{i} дан" for i in range(1, 10)]

    def create_top_buttons(self):
        buttons_frame = tk.Frame(self)
        back_button = ttk.Button(buttons_frame, text="\u2190", command=self.back, width=10)
        add_category = ttk.Button(buttons_frame, text="Добавить категорию",
                                  command=self.open_add_change_category_window, width=20)

        back_button.pack(side="left")
        add_category.pack(side="left", padx=5)

        buttons_frame.pack(fill="both", pady=(0, 10))

    def create_category_table(self):
        self.category_table = self.create_table(
            label_text="Параметры",
            headers=['№', 'Пол', 'Возраст', 'Категория', 'Участников', 'Совпадений', 'ID'])
        self.category_table.bind("<Double-1>", self.on_double_click)
        # self.category_table.bind('<Button-3>', self.right_button_menu)

    def create_unallocated_table(self):
        self.unallocated_table = self.create_table(
            label_text="Не распределенные",
            headers=['ID', 'ФИО', 'Полных лет', 'Категория', 'Город', 'Тренер'],
            padx=10)

    def create_athletes_table(self):
        self.athletes_table = self.create_table(
            label_text="Участники",
            headers=['ID', 'ФИО', 'Полных лет', 'Категория', 'Город', 'Тренер'])

    def create_table(self, label_text, headers, padx=0):
        frame = tk.Frame(self, bd=1, relief="sunken")
        frame.pack(side="left", fill="both", expand=True, padx=padx)
        label = tk.Label(frame, text=label_text, font=("Arial", 14), width=20)
        label.pack(side="top", pady=(5, 2))

        table = ttk.Treeview(frame, columns=headers, show='headings')

        total_width = frame.winfo_reqwidth() or 1
        col_width = total_width // len(headers)
        for header in headers:
            table.heading(header, text=header)
            if header == 'ID':
                table.column(header, stretch=False, anchor='center', minwidth=30, width=30)
            else:
                table.column(header, width=col_width, anchor='center')

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscroll=scrollbar.set)

        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return table

    def right_button_menu(self, event):
        item = self.category_table.identify_row(event.y)
        if item:
            self.category_table.selection_set(item)
            self.category_table.focus(item)
            values = self.category_table.item(item, "values")

        event.widget.focus()
        file_menu = tk.Menu(self)
        file_menu.add_command(label='Изменить', command=lambda: self.open_add_change_window(change=True, num=values[0]))
        file_menu.add_command(label='Удалить', command=lambda: self.delete_competition(values[0]))
        file_menu.post(event.x_root, event.y_root)

    def on_double_click(self, event):
        item = self.category_table.identify_row(event.y)
        if item:
            values = self.category_table.item(item, "values")
            self.load_athletes_table(values[0])

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
        entries = [ttk.Combobox(frame, values=ages, state="readonly", width=30) for _ in range(2)]
        entries += [ttk.Combobox(frame, values=self.categories, state="readonly", width=30) for _ in range(2)]
        entries.insert(0, ttk.Combobox(frame, values=['муж', 'жен'], state="readonly"))

        tk.Label(frame, text="Пол:").grid(row=0, column=0, sticky="w", pady=(0, 10))
        entries[0].grid(row=0, column=1, columnspan=3, sticky="ew", pady=(0, 10))

        tk.Label(frame, text="Возраст от:").grid(row=1, column=0, sticky="w", pady=(0, 10))
        tk.Label(frame, text="до:").grid(row=1, column=2, sticky="w", pady=(0, 10), padx=(10, 0))
        entries[1].grid(row=1, column=1, sticky="w", pady=(0, 10))
        entries[1].bind("<<ComboboxSelected>>", lambda x: self.update_entry_ages(entries[1], entries[2]))
        entries[2].grid(row=1, column=3, sticky="w", pady=(0, 10))

        tk.Label(frame, text="Категория от:").grid(row=2, column=0, sticky="w")
        tk.Label(frame, text="до:").grid(row=2, column=2, sticky="w", padx=(10, 0))
        entries[3].grid(row=2, column=1, sticky="w")
        entries[3].bind("<<ComboboxSelected>>", lambda x: self.update_entry_categoties(entries[3], entries[4]))
        entries[4].grid(row=2, column=3, sticky="w")

        buttons_frame = tk.Frame(frame)
        buttons_frame.grid(columnspan=4, row=3, pady=20, sticky="ew")

        if change:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tyli WHERE competition_id =?", (compet_id,))
                values = cursor.fetchone()
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
        parameters = ()
        for i, entry in enumerate(entries):
            if i > 2:
                parameters += (self.categories.index(entry.get()),)
            else:
                parameters += (entry.get(),)
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                if change:
                    parameters += (cat_id,)
                    cursor.execute(
                        "UPDATE tyli SET gender = ?, age_form = ?, age_to = ?, category_from = ?, category_to = ? WHERE id = ?",
                        parameters)
                else:
                    parameters += (self.current_id,)
                    cursor.execute(
                        "INSERT INTO tyli (gender, age_form, age_to, category_from, category_to, competition_id) VALUES (?, ?, ?, ?, ?, ?)",
                        parameters)
                conn.commit()
            self.load_unallocated_table()
            self.load_category_table(self.current_id)
            self.top_window.destroy()
        except Exception as e:
            self.top_window.destroy()
            messagebox.showerror("Ошибка", f"{e}", parent=self.master)

    @staticmethod
    def update_entry_ages(entry_from, entry_to):
        entry_to['values'] = [str(i) for i in range(int(entry_from.get()), 100)]
        if entry_to.get() and int(entry_from.get()) > int(entry_to.get()):
            entry_to.set('')

    def update_entry_categoties(self, entry_from, entry_to):
        entry_to['values'] = self.categories[self.categories.index(entry_from.get()):]
        if entry_to.get() and self.categories.index(entry_from.get()) > self.categories.index(entry_to.get()):
            entry_to.set('')

    def load_category_table(self, comp_id):
        self.current_id = comp_id
        for row in self.category_table.get_children():
            self.category_table.delete(row)
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tyli WHERE competition_id = ?", (self.current_id,))
            tyli_data = cursor.fetchall()
        for num, row in enumerate(tyli_data):
            athletes_count = 0
            unallocated_count = 0
            values = [num + 1, row[2], f'{row[3]} - {row[4]}',
                      f'{self.categories[row[5]]} - {self.categories[row[6]]}',
                      athletes_count, unallocated_count, [row[0]]]
            self.category_table.insert("", tk.END, values=values)

    def load_athletes_table(self, tyli_id):
        for row in self.athletes_table.get_children():
            self.athletes_table.delete(row)

        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tyli WHERE id = ?", (tyli_id,))
                data = cursor.fetchall()[0]
                parameters = (self.current_id,) + data[2:-1] + ('да',)
                cursor.execute("""SELECT * FROM athletes WHERE competition_id = ?
                                        AND  gender = ?
                                        AND age BETWEEN ? AND ?
                                        AND  category BETWEEN ? AND ?
                                        AND tyli= ?
                                    """, parameters)

                athletes = cursor.fetchall()
            for num, row in enumerate(athletes):
                values = [row[0], row[2], row[5], self.categories[row[7]], row[8], row[10]]
                self.athletes_table.insert("", tk.END, values=values)
            print(len(athletes))
        except Exception as e:
            messagebox.showerror("Ошибка", f"{e}", parent=self.master)

    def load_unallocated_table(self):
        conn = sqlite3.connect(config.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tyli WHERE competition_id = ?", (self.current_id,))
        data = cursor.fetchall()
