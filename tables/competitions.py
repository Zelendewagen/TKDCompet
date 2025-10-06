import sqlite3
from datetime import datetime
from tkinter import ttk, messagebox
import tkinter as tk

import config
from config import DB_FILE


class CompetitionsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_top_buttons()
        self.create_table()

    def create_top_buttons(self):
        buttons_frame = tk.Frame(self)
        back_button = ttk.Button(buttons_frame, text="Создать новое соревнование", command=self.open_add_change_window)
        back_button.pack(side="left")

        buttons_frame.pack(fill="both", pady=(0, 10))

    def create_table(self):
        heads = ['ID', 'Название соревнования', 'Дата', 'Город', 'Клуб']
        self.table = ttk.Treeview(self, columns=heads, show='headings', selectmode="browse")
        for header in heads:
            self.table.heading(header, text=header, anchor='w')
        self.table.column('ID', stretch=False, minwidth=50, width=50)
        self.table.column('Название соревнования', stretch=False, width=400, minwidth=150)
        self.table.column('Дата', stretch=False, minwidth=150, width=150)
        self.table.column('Город', stretch=False, minwidth=150, width=150)
        self.table.column('Клуб', stretch=True)
        self.table.bind('<Button-3>', self.right_button_menu)
        self.table.bind("<Double-1>", self.on_double_click)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def right_button_menu(self, event):
        item = self.table.identify_row(event.y)
        if item:
            self.table.selection_set(item)
            self.table.focus(item)
            values = self.table.item(item, "values")

        event.widget.focus()
        file_menu = tk.Menu(self)
        file_menu.add_command(label='Изменить', command=lambda: self.open_add_change_window(change=True, num=values[0]))
        file_menu.add_command(label='Удалить', command=lambda: self.delete_competition(values[0]))
        file_menu.post(event.x_root, event.y_root)

    def on_double_click(self, event):
        item = self.table.identify_row(event.y)
        if item:
            values = self.table.item(item, "values")
            self.show_athletes_table(values[0])

    def open_add_change_window(self, change=False, num=None):
        self.top_window = tk.Toplevel()
        self.top_window.grab_set()
        title = 'Изменить соревнование' if change else 'Создать соревнование'
        self.top_window.title(title)
        self.top_window.geometry(config.geometry(self.master, config.cmp_window_width, config.cmp_window_height))
        self.top_window.resizable(False, False)
        self.top_window.transient(self)

        frame = tk.Frame(self.top_window)
        frame.pack(fill="both", padx=(10, 50), pady=10, expand=True)
        frame.columnconfigure(index=1, weight=250)

        labels = ['Название', 'Дата', 'Город', 'Клуб', 'Гл. судья', 'Судья', 'Секретарь']

        for i, text in enumerate(labels):
            label = tk.Label(frame, text=text)
            if i == len(labels) - 1:
                label.grid(column=0, row=i, sticky='w')
            else:
                label.grid(column=0, row=i, sticky='w', pady=(0, 10))

        entries = [tk.Entry(frame, width=30) for _ in range(len(labels))]
        for i, entry in enumerate(entries):
            if i + 1 == len(entries):
                entries[i].grid(column=1, row=i, sticky='ew')
            else:
                entries[i].grid(column=1, row=i, sticky='ew', pady=(0, 10))

        buttons_frame = tk.Frame(frame)
        buttons_frame.grid(columnspan=2, row=len(labels), pady=20, padx=(20, 0), sticky="ew")

        if change:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM competitions WHERE id =?", (num,))
                values = cursor.fetchone()
            for i, entry in enumerate(entries):
                entries[i].insert(0, values[i + 1])

            change_button = ttk.Button(buttons_frame, text='Изменить', width=15,
                                       command=lambda: self.add_change_comp(entries, comp_id=values[0], change=True))
            change_button.pack(fill="both", expand=True, side="left", padx=5)
        else:
            add_button = ttk.Button(buttons_frame, text='Добавить', width=15,
                                    command=lambda: self.add_change_comp(entries))
            add_button.pack(fill="both", expand=True, side="left", padx=5)

        cancel_button2 = ttk.Button(buttons_frame, text="Отмена", command=self.top_window.destroy, width=15)
        cancel_button2.pack(fill="both", expand=True, side="left", padx=5)

    def add_change_comp(self, entries, comp_id=None, change=False):
        parameters = ()
        for i in entries:
            parameters += (i.get(),)
        try:
            datetime.strptime(parameters[1], "%d.%m.%Y")
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                if change:
                    parameters += (comp_id,)
                    cursor.execute("UPDATE competitions"
                                   " SET name = ?, date = ?, location = ?, club = ?, main_judge = ?, judge = ?, secretary= ? WHERE id = ?",
                                   parameters)
                    self.master.athletes_frame.update_ages(comp_id)
                else:
                    cursor.execute(
                        "INSERT INTO competitions (name, date, location, club, main_judge, judge, secretary) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        parameters)
                conn.commit()

            self.update_table()
            self.top_window.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Не верный формат даты!", parent=self.master)

    def delete_competition(self, num):
        answer = messagebox.askyesno("Удалить соревнование", "УДАЛИТЬ?")
        if answer:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM competitions WHERE id = ?", (num,))
                cursor.execute("DELETE FROM athletes WHERE competition_id = ?", (num,))
                conn.commit()
            self.update_table()

    def update_table(self):
        for row in self.table.get_children():
            self.table.delete(row)
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM competitions")
            competitions = cursor.fetchall()
        for row in competitions:
            self.table.insert("", tk.END, values=row[:-3])

    def show_athletes_table(self, comp_id):
        self.master.show_table('спортсмены', self)
        self.master.athletes_frame.load_table(comp_id)
