import sqlite3
from tkinter import ttk
import tkinter as tk

from config import DB_FILE


class AthletesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        heads = ['№', 'ФИО', 'Пол', 'Дата рождения', 'Полных лет', 'Вес', 'Категория', 'Регион', 'Тренер', 'Массоги',
                 'Тыли']
        self.table = ttk.Treeview(self, columns=heads, show='headings', selectmode="browse")
        for header in heads:
            self.table.heading(header, text=header, anchor='w')
        self.table.column('№', stretch=False, minwidth=50, width=50)
        self.table.column('ФИО', minwidth=150)
        self.table.column('Пол', stretch=False, minwidth=80, width=80)
        self.table.column('Дата рождения', stretch=False, minwidth=80, width=100)
        self.table.column('Полных лет', stretch=False, minwidth=80, width=80)
        self.table.column('Вес', stretch=False, minwidth=50, width=50)
        self.table.column('Категория', stretch=False, minwidth=80, width=80)
        self.table.column('Регион', stretch=True, minwidth=80, width=80)
        self.table.column('Тренер', stretch=True, minwidth=80, width=80)
        self.table.column('Массоги', stretch=True, minwidth=80, width=80)
        self.table.column('Тыли', stretch=True, minwidth=80, width=80)
        self.table.bind('<Button-3>', self.right_button_menu)
        self.table.bind("<Double-1>", self.on_double_click)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=self.scrollbar.set)

        buttons_frame = tk.Frame(self)
        back_button = tk.Button(buttons_frame, text="\u2190", command=self.show_competitions_table)
        add_button = tk.Button(buttons_frame, text="Добавить одного")
        add_list_button = tk.Button(buttons_frame, text="Добавить список")

        back_button.pack(side="left", padx=5, pady=5, ipadx=10)
        add_button.pack(side="left", padx=5, pady=5)
        add_list_button.pack(side="left", padx=5, pady=5)

        buttons_frame.pack(fill="both", padx=5)
        self.table.pack(side="left", fill="both", padx=10, pady=10, expand=True)
        self.scrollbar.pack(side="right", fill="y", pady=10)

    def right_button_menu(self, event):
        item = self.table.identify_row(event.y)
        if item:
            self.table.selection_set(item)
            self.table.focus(item)

        popup_menu = tk.Menu(self)
        event.widget.focus()
        file_menu = tk.Menu(popup_menu)
        file_menu.add_command(label='Изменить', command=lambda: print(self.table.item(item).get('values')))
        file_menu.add_separator()
        file_menu.add_command(label='Удалить')
        file_menu.post(event.x_root, event.y_root)

    def on_double_click(self, event):
        item = self.table.identify_row(event.y)
        if item:
            values = self.table.item(item, "values")

    def load_table(self, id):
        for row in self.table.get_children():
            self.table.delete(row)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM athletes WHERE competition_id = ?", (id,))
        athletes = cursor.fetchall()
        conn.close()
        for row in athletes:
            values = [i for i in row if i != 1]
            self.table.insert("", tk.END, values=values)

    def show_competitions_table(self):
        for widget in self.master.winfo_children():
            if not widget.winfo_ismapped():
                widget.pack(fill="both", expand=True)
        self.pack_forget()
