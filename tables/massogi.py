import os
import sqlite3
from datetime import datetime
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter.filedialog import askopenfilename

import pandas as pd

import config
from config import DB_FILE


class MassogiFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.category_table = None
        self.unallocated_talbe = None
        self.athletes_table = None

        self.current_id = None
        self.create_top_buttons()
        self.create_category_table()
        self.create_unallocated_talbe()
        self.create_athletes_table()

    def create_top_buttons(self):
        buttons_frame = tk.Frame(self)
        back_button = ttk.Button(buttons_frame, text="\u2190", command=self.back, width=10)
        add_category = ttk.Button(buttons_frame, text="Добавить категорию", command=self.add_category, width=20)

        back_button.pack(side="left", padx=5, pady=5)
        add_category.pack(side="left", padx=5, pady=5)

        buttons_frame.pack(fill="both", padx=5, pady=(10, 0))

    def create_category_table(self):
        frame = tk.Frame(self)

        heads = ['Пол', 'Возраст', 'Категория', 'Вес']
        self.category_table = ttk.Treeview(frame, columns=heads, show='headings', selectmode="browse")
        table = self.category_table
        for header in heads:
            table.heading(header, text=header, anchor='w')
        table.column('Пол', stretch=False, minwidth=50, width=50)
        table.column('Возраст', minwidth=50, width=50)
        table.column('Категория', stretch=False, minwidth=80, width=80)

        # self.table.bind('<Button-3>', self.right_button_menu)
        # self.table.bind("<Double-1>", self.on_double_click)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscroll=scrollbar.set)
        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        frame.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

    def create_unallocated_talbe(self):
        frame = tk.Frame(self)
        heads = ['Пол', 'Возраст', 'Категория']
        self.unallocated_talbe = ttk.Treeview(frame, columns=heads, show='headings', selectmode="browse")
        table = self.unallocated_talbe
        for header in heads:
            table.heading(header, text=header, anchor='w')
        table.column('Пол', stretch=False, minwidth=50, width=50)
        table.column('Возраст', minwidth=50, width=50)
        table.column('Категория', stretch=False, minwidth=80, width=80)

        # self.table.bind('<Button-3>', self.right_button_menu)
        # self.table.bind("<Double-1>", self.on_double_click)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscroll=scrollbar.set)
        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        frame.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

    def create_athletes_table(self):
        frame = tk.Frame(self)
        heads = ['Пол', 'Возраст', 'Категория']
        self.athletes_table = ttk.Treeview(frame, columns=heads, show='headings', selectmode="browse")
        table = self.athletes_table
        for header in heads:
            table.heading(header, text=header, anchor='w')
        table.column('Пол', stretch=False, minwidth=50, width=50)
        table.column('Возраст', minwidth=50, width=50)
        table.column('Категория', stretch=False, minwidth=80, width=80)

        # self.table.bind('<Button-3>', self.right_button_menu)
        # self.table.bind("<Double-1>", self.on_double_click)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscroll=scrollbar.set)
        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        frame.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

    def add_category(self):
        pass

    def back(self):
        self.master.show_table('спортсмены', self)
