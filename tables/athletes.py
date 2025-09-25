import os
import sqlite3
from datetime import datetime
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter.filedialog import askopenfilename

import pandas as pd

import config
from config import DB_FILE


class AthletesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        heads = ['№', 'ФИО', 'Пол', 'Дата рождения', 'Полных лет', 'Вес', 'Категория', 'Регион', 'Клуб', 'Тренер',
                 'Тыли', 'Массоги', 'ID']
        self.current_id = None
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
        self.table.column('Клуб', stretch=True, minwidth=80, width=80)
        self.table.column('Тренер', stretch=True, minwidth=80, width=80)
        self.table.column('Тыли', stretch=True, minwidth=80, width=80)
        self.table.column('Массоги', stretch=True, minwidth=80, width=80)
        self.table.column('ID', stretch=False, minwidth=50, width=50)
        self.table.bind('<Button-3>', self.right_button_menu)
        self.table.bind("<Double-1>", self.on_double_click)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=self.scrollbar.set)

        buttons_frame = tk.Frame(self)
        back_button = ttk.Button(buttons_frame, text="\u2190", command=self.show_competitions_table, width=10)
        add_button = ttk.Button(buttons_frame, text="Добавить участника", command=self.open_add_change_athlete_window,
                                width=20)
        add_list_button = ttk.Button(buttons_frame, text="Добавить список", command=self.add_list_athletes, width=20)
        clear_list_button = ttk.Button(buttons_frame, text="Удалить всех", command=self.clear_list_athletes, width=20)

        back_button.pack(side="left", padx=5, pady=5)
        add_button.pack(side="left", padx=5, pady=5)
        add_list_button.pack(side="left", padx=5, pady=5)
        clear_list_button.pack(side="left", padx=5, pady=5)

        buttons_frame.pack(fill="both", padx=5, pady=(10, 0))
        self.table.pack(side="left", fill="both", padx=10, pady=10, expand=True)
        self.scrollbar.pack(side="right", fill="y", pady=10)

    def right_button_menu(self, event):
        item = self.table.identify_row(event.y)
        if item:
            self.table.selection_set(item)
            self.table.focus(item)
            values = self.table.item(item, "values")

        event.widget.focus()
        file_menu = tk.Menu(self)
        file_menu.add_command(label='Изменить',
                              command=lambda: self.open_add_change_athlete_window(change=True, athlete_id=values[-1]))
        file_menu.add_separator()
        file_menu.add_command(label='Удалить', command=lambda: self.delete_athlete(values[-1]))
        file_menu.post(event.x_root, event.y_root)

    def on_double_click(self, event):
        item = self.table.identify_row(event.y)
        if item:
            values = self.table.item(item, "values")
            self.open_add_change_athlete_window(change=True, athlete_id=values[-1])

    def load_table(self, comp_id):
        self.current_id = comp_id
        for row in self.table.get_children():
            self.table.delete(row)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM athletes WHERE competition_id = ?", (self.current_id,))
        athletes = cursor.fetchall()
        conn.close()
        for num, row in enumerate(athletes):
            values = [num + 1] + [i for i in row[2:]] + [row[0]]
            self.table.insert("", tk.END, values=values)

    def show_competitions_table(self):
        for widget in self.master.winfo_children():
            if not widget.winfo_ismapped():
                widget.pack(fill="both", expand=True)
        self.pack_forget()

    def add_list_athletes(self):
        file = askopenfilename(title='Открыть', filetypes=(("Таблица Excel", "*.xls"),))
        if file:
            xls = pd.ExcelFile(file)
            sheet_names = xls.sheet_names
            data = []
            sheets = []
            for sheet in sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet)
                if not df.dropna(how="all").empty:
                    data = df.values.tolist()
                    sheets.append(sheet)
            if data:
                if len(sheets) == 1:
                    conn = sqlite3.connect(config.DB_FILE)
                    cursor = conn.cursor()
                    for row in data:
                        cursor.execute("SELECT date FROM competitions WHERE id = ?", (self.current_id,))
                        birth_date = datetime.strptime(row[3].strftime("%d.%m.%Y"), "%d.%m.%Y")
                        compet_date = datetime.strptime(cursor.fetchone()[0], "%d.%m.%Y")
                        age = compet_date.year - birth_date.year
                        if (compet_date.month, compet_date.day) < (birth_date.month, birth_date.day):
                            age -= 1
                        parameters = (
                            self.current_id, row[2], row[1], row[3].strftime("%d.%m.%Y"), age, int(float(row[4])),
                            row[6], row[8], row[11], row[12], row[13], row[14])
                        cursor.execute(
                            "INSERT INTO athletes (competition_id, name, gender, date, age, weight, category, region, club, trainer, tyli, massogi) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                            parameters)
                    conn.commit()
                    cursor.close()
                    self.load_table(self.current_id)
                    messagebox.showinfo("Готово", f"Участники загружены из {os.path.basename(file)} {sheets[0]}")
                else:
                    messagebox.showerror("Ошибка", f"Загрузка отменена, проверьте {', '.join(map(str, sheets))}")
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить")

    def clear_list_athletes(self):
        answer = messagebox.askyesno("Удалить всех участников", "Удалить ВСЕХ участников?")
        if answer:
            conn = sqlite3.connect(config.DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM athletes WHERE competition_id = ?", (self.current_id,))
            conn.commit()
            cursor.close()
            self.load_table(self.current_id)

    def delete_athlete(self, athlete_id):
        answer = messagebox.askyesno("Удалить участника", "УДАЛИТЬ?")
        if answer:
            conn = sqlite3.connect(config.DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM athletes WHERE id = ?", (athlete_id,))
            conn.commit()
            cursor.close()
            self.load_table(self.current_id)

    def open_add_change_athlete_window(self, change=False, athlete_id=None):
        self.top_window = tk.Toplevel()
        self.top_window.grab_set()
        self.top_window.title('Изменить участника')
        self.top_window.geometry(config.geometry(self.master, config.athl_window_width, config.athl_window_height))
        self.top_window.resizable(False, False)
        self.top_window.attributes("-topmost", True)

        frame = tk.Frame(self.top_window)
        frame.pack(fill="both", padx=(10, 50), pady=10, expand=True)
        frame.columnconfigure(index=1, weight=250)

        labels = ['ФИО', 'Пол', 'Дата рождения', 'Вес', 'Категория', 'Регион', 'Клуб', 'Тренер', 'Тыли', 'Массоги']
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
        buttons_frame.grid(columnspan=2, row=len(labels), pady=20, padx=100, sticky="ew")

        if change:
            conn = sqlite3.connect(config.DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM athletes WHERE id =?", (athlete_id,))
            values = cursor.fetchone()
            conn.close()
            for i, entry in enumerate(entries):
                if i >= 3:
                    entries[i].insert(0, values[i + 3])
                else:
                    entries[i].insert(0, values[i + 2])

            change_button = ttk.Button(buttons_frame, text='Изменить', width=15,
                                       command=lambda:
                                       self.add_change_athlete(entries, athlete_id=values[0], change=True))
            change_button.pack(fill="both", expand=True, side="left", padx=5)
        else:
            add_button = ttk.Button(buttons_frame, text='Добавить', width=15,
                                    command=lambda: self.add_change_athlete(entries))
            add_button.pack(fill="both", expand=True, side="left", padx=5)

        cancel_button2 = ttk.Button(buttons_frame, text="Отмена", command=self.top_window.destroy, width=15)
        cancel_button2.pack(fill="both", expand=True, side="left", padx=5)

    def add_change_athlete(self, entries, athlete_id=None, change=False):
        parameters = ()
        for i in entries:
            parameters += (i.get(),)
        try:
            datetime.strptime(parameters[2], "%d.%m.%Y")
            conn = sqlite3.connect(config.DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT date FROM competitions WHERE id = ?", (self.current_id,))
            birth_date = datetime.strptime(parameters[2], "%d.%m.%Y")
            compet_date = datetime.strptime(cursor.fetchone()[0], "%d.%m.%Y")
            age = compet_date.year - birth_date.year
            if (compet_date.month, compet_date.day) < (birth_date.month, birth_date.day):
                age -= 1
            parameters += (age,)
            if change:
                parameters += (athlete_id,)
                cursor.execute("UPDATE athletes"
                               " SET name = ?, gender = ?, date = ?, weight = ?, category = ?, region = ?, club = ?, trainer = ?, tyli = ?, massogi = ?, age = ? WHERE id = ?",
                               parameters)
            else:
                parameters += (self.current_id,)
                cursor.execute(
                    "INSERT INTO athletes (name, gender, date, weight, category, region, club, trainer, tyli, massogi, age, competition_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    parameters)
            conn.commit()
            cursor.close()
            self.load_table(self.current_id)
            self.top_window.destroy()
        except ValueError:
            self.top_window.destroy()
            messagebox.showerror("Ошибка", "Не верный формат даты!", parent=self.master)

    def update_ages(self, comp_id):
        with sqlite3.connect(config.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, date FROM athletes WHERE competition_id = ?", (comp_id,))
            rows = cursor.fetchall()
            cursor.execute("SELECT date FROM competitions WHERE id = ?", (comp_id,))
            compet_date = datetime.strptime(cursor.fetchone()[0], "%d.%m.%Y")
            for ath_id, date in rows:
                birth_date = datetime.strptime(date, "%d.%m.%Y")
                age = compet_date.year - birth_date.year
                if (compet_date.month, compet_date.day) < (birth_date.month, birth_date.day):
                    age -= 1
                cursor.execute("UPDATE athletes SET age = ? WHERE id = ?", (age, ath_id))


