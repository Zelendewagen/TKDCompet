import sqlite3
from tkinter import ttk, messagebox
import tkinter as tk

import config


class CompetitionsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        heads = ['№', 'Название соревнования', 'Дата', 'Город', 'Клуб']
        self.table = ttk.Treeview(self, columns=heads, show='headings', selectmode="browse")
        for header in heads:
            self.table.heading(header, text=header, anchor='w')
        self.table.column('№', stretch=False, minwidth=50, width=50)
        self.table.column('Название соревнования', stretch=True, width=150, minwidth=110)
        self.table.column('Дата', stretch=False, minwidth=150, width=150)
        self.table.column('Город', stretch=False, minwidth=150, width=150)
        self.table.column('Клуб', stretch=True, width=150, minwidth=110)
        self.table.bind('<Button-3>', self.right_button_menu)
        self.table.bind("<Double-1>", self.on_double_click)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=self.scrollbar.set)

        buttons_frame = tk.Frame(self)
        back_button = ttk.Button(buttons_frame, text="Создать новое соревнование", command=self.open_add_change_window)
        back_button.pack(side="left", padx=5, pady=5)

        buttons_frame.pack(fill="both", padx=5, pady=(10, 0))
        self.table.pack(side="left", fill="both", padx=10, pady=10, expand=True)
        self.scrollbar.pack(side="right", fill="y")

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

    def show_athletes_table(self, name):
        for child in self.master.winfo_children():
            if not child.winfo_ismapped():
                child.pack(fill="both", expand=True)
                child.load_table(name)
        self.pack_forget()

    def update_table(self):
        for row in self.table.get_children():
            self.table.delete(row)
        conn = sqlite3.connect(config.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM competitions")
        competitions = cursor.fetchall()
        conn.close()
        for row in competitions:
            self.table.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4]))

    def open_add_change_window(self, change=False, num=None):
        window = tk.Toplevel()
        window.grab_set()
        window.title('Создать соревнование')
        window.geometry(config.geometry(self.master, config.top_width, config.top_height))
        window.resizable(False, False)
        window.attributes("-topmost", True)

        frame = tk.Frame(window)
        frame.pack(fill="both", padx=(10, 50), pady=10, expand=True)
        frame.columnconfigure(index=0)
        frame.columnconfigure(index=1, weight=250)

        name = tk.Label(frame, text='Название')
        date = tk.Label(frame, text='Дата')
        location = tk.Label(frame, text='Город')
        club = tk.Label(frame, text='Клуб')
        main_judge = tk.Label(frame, text='Гл. судья')
        judge = tk.Label(frame, text='Судья')
        secretary = tk.Label(frame, text='Секретарь')
        name.grid(column=0, row=0, sticky='w', pady=(0, 10))
        date.grid(column=0, row=1, sticky='w', pady=(0, 10))
        location.grid(column=0, row=2, sticky='w', pady=(0, 10))
        club.grid(column=0, row=3, sticky='w', pady=(0, 10))
        main_judge.grid(column=0, row=4, sticky='w', pady=(0, 10))
        judge.grid(column=0, row=5, sticky='w', pady=(0, 10))
        secretary.grid(column=0, row=6, sticky='w')

        entries = [tk.Entry(frame, width=30) for _ in range(7)]
        for i, entry in enumerate(entries):
            if i + 1 == len(entries):
                entries[i].grid(column=1, row=i, sticky='ew')
            else:
                entries[i].grid(column=1, row=i, sticky='ew', pady=(0, 10))

        buttons_frame = tk.Frame(frame)
        buttons_frame.grid(columnspan=2, row=7, pady=20, padx=100, sticky="ew")

        if change:
            conn = sqlite3.connect(config.DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM competitions WHERE id =?", (num,))
            values = cursor.fetchone()
            conn.close()
            for i, entry in enumerate(entries):
                entries[i].insert(0, values[i + 1])

            change_button = ttk.Button(buttons_frame, text='Изменить', width=15,
                                       command=lambda: (
                                           self.change_competition(entries, num=values[0]), window.destroy()))
            change_button.pack(fill="both", expand=True, side="left", padx=5)
        else:
            add_button = ttk.Button(buttons_frame, text='Добавить', width=15,
                                    command=lambda: (self.create_competition(entries), window.destroy()))
            add_button.pack(fill="both", expand=True, side="left", padx=5)

        cancel_button2 = ttk.Button(buttons_frame, text="Отмена", command=window.destroy, width=15)
        cancel_button2.pack(fill="both", expand=True, side="left", padx=5)

    def create_competition(self, entries):
        parameters = ()
        for i in entries:
            parameters += (i.get(),)
        conn = sqlite3.connect(config.DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO competitions (name, date, location, club, main_judge, judge, secretary) VALUES (?, ?, ?, ?, ?, ?, ?)",
            parameters)
        conn.commit()
        cursor.close()
        self.update_table()

    def change_competition(self, entries, num):
        parameters = ()
        for i in entries:
            parameters += (i.get(),)
        parameters += (num,)

        conn = sqlite3.connect(config.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE competitions"
                       " SET name = ?, date = ?, location = ?, club = ?, main_judge = ?, judge = ?, secretary= ? WHERE id = ?",
                       parameters)
        conn.commit()
        cursor.close()
        self.update_table()

    def delete_competition(self, num):
        answer = messagebox.askyesno("Удалить соревнование", "УДАЛИТЬ?")
        if answer:
            conn = sqlite3.connect(config.DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM competitions WHERE id = ?", (num,))
            conn.commit()
            cursor.close()
            self.update_table()
