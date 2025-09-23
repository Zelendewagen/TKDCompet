from tkinter import ttk
import tkinter as tk


class CompetitionsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        heads = ['№', 'Дата', 'Место проведения', 'Название соревнования', 'Клуб']
        self.table = ttk.Treeview(self, columns=heads, show='headings', selectmode="browse")
        for header in heads:
            self.table.heading(header, text=header, anchor='w')
        self.table.column('№', stretch=False, minwidth=50, width=50)
        self.table.column('Дата', stretch=False, minwidth=150, width=150)
        self.table.column('Место проведения', stretch=False, minwidth=150, width=150)
        self.table.column('Название соревнования', stretch=True, width=150, minwidth=110)
        self.table.column('Клуб', stretch=True, width=150, minwidth=110)
        self.table.bind('<Button-3>', self.right_button_menu)
        self.table.bind("<Double-1>", self.on_double_click)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=self.scrollbar.set)

        self.table.pack(side="left", fill="both", padx=10, pady=10, expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def right_button_menu(self, event):
        item = self.table.identify_row(event.y)
        if item:
            self.table.selection_set(item)
            self.table.focus(item)

        popup_menu = tk.Menu(self)
        event.widget.focus()
        file_menu = tk.Menu(popup_menu)
        file_menu.add_command(label='Изменить', command=lambda: print(self.item(item).get('values')))
        file_menu.add_separator()
        file_menu.add_command(label='Удалить')
        file_menu.post(event.x_root, event.y_root)

    def on_double_click(self, event):
        item = self.table.identify_row(event.y)
        if item:
            values = self.table.item(item, "values")
            print(values)
        self.show_athletes_table(values[0])

    def show_athletes_table(self, name):
        print(name)
        for widget in self.master.winfo_children():
            if not widget.winfo_ismapped():
                widget.pack(fill="both", expand=True)
        self.pack_forget()
