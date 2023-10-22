import tkinter as tk
import sqlite3
from tkinter import ttk


# Создание основного приложения
class Main(tk.Frame):
    # Инициализация класса
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Добавление в бд параметров
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    # Подключение к классу обновления
    def open_update_dialog(self):
        Update()

    # Подключение к классу поиска
    def open_search_dialog(self):
        Search()

    # Отображение результатов поиска
    def search_records(self, name):
        self.db.c.execute("SELECT * FROM db WHERE name LIKE ?", ("%" + name + "%", ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=i) for i in self.db.c.fetchall()]

    # Отображение результатов удаления
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute("""DELETE FROM db WHERE id=?""", (self.tree.set(selection_item, '#1'),))
            self.db.conn.commit()
            self.view_records()

    # Обновление данных базы данных
    def update_records(self, name, tel, email, salary):
        self.db.c.execute("""UPDATE db SET name=?, tel=?, email=?, salary=?
        WHERE ID=?""", (name, tel, email, salary,
                        self.tree.set(self.tree.selection()[0], "#1")))
        self.db.conn.commit()
        self.view_records()

    # Создание основного окна приложения
    def init_main(self):
        # Создание полоски с кнопками управления приложением
        toolbar = tk.Frame(bg='#ff6161', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления пользователя
        self.add_img = tk.PhotoImage(file='./img/add.png')

        btn_open_dialog = tk.Button(toolbar, bg='#ff6161', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        # Отрисовка базы данных
        self.tree = ttk.Treeview(columns=("ID", "name", "tel", "email", "salary",), height=45, show="headings")

        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=260, anchor=tk.CENTER)
        self.tree.column("tel", width=130, anchor=tk.CENTER)
        self.tree.column("email", width=130, anchor=tk.CENTER)
        self.tree.column("salary", width=130, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="Зарплата")

        self.tree.pack(side=tk.LEFT)

        # Кнопка обновления данных о пользователе
        self.update_img = tk.PhotoImage(file='./img/refactor.png')
        btn_open_update_dialog = tk.Button(toolbar, bg="#ff6161", bd=0, image=self.update_img,
                                           command=self.open_update_dialog)

        btn_open_update_dialog.pack(side=tk.LEFT)

        # Кнопка удаления пользователя
        self.delete_button_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg="#ff6161", bd=0, image=self.delete_button_img, command=self.delete_records)

        btn_delete.pack(side=tk.LEFT)

        # Кнопка поиска пользователя по имени
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg="#ff6161", bd=0, image=self.search_img, command=self.open_search_dialog)

        btn_search.pack(side=tk.LEFT)

        # Кнопка обновления базы данных
        self.refresh_img = tk.PhotoImage(file="./img/refresh.png")
        btn_refresh = tk.Button(toolbar, bg="#ff6161", bd=0, image=self.refresh_img, command=self.view_records)

        btn_refresh.pack(side=tk.LEFT)

    # Связь с дочерним окном
    def open_dialog(self):
        Child()

    # Вывод базы данных
    def view_records(self):
        self.db.c.execute('''SELECT * FROM db''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', "end", values=row) for row in self.db.c.fetchall()]


# Дочернее окно
class Child(tk.Toplevel):
    # Инициализация
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Созданияе дочернего окна для добавления пользователя
    def init_child(self):
        # Основные параметры
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # Отрисовка названий полей ввода
        lable_name = tk.Label(self, text="ФИО: ")
        lable_name.place(x=50, y=50)
        lable_name = tk.Label(self, text="Телефон: ")
        lable_name.place(x=50, y=80)
        lable_name = tk.Label(self, text="E-mail: ")
        lable_name.place(x=50, y=110)
        lable_name = tk.Label(self, text="Зарплата: ")
        lable_name.place(x=50, y=140)

        # Создание полей для ввода
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=180, y=50)

        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=180, y=80)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=180, y=110)

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=180, y=140)

        # Кнопка закрыть окно
        self.btn_canseled = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_canseled.place(x=300, y=170)

        # Кнопка добавить пользователя
        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=210, y=170)

        self.btn_add.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                        self.entry_email.get(),
                                                                        self.entry_tel.get(),
                                                                        self.entry_salary.get()))


# Обновление данных о пользователе
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.defoult_data()

    # Функция редактирования данных
    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_records(self.entry_name.get(),
                                                                           self.entry_email.get(),
                                                                           self.entry_tel.get(),
                                                                           self.entry_salary.get()))

        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_add.destroy()

    # Функция отрисовки старых значений в поля изменения пользоветяеля
    def defoult_data(self):
        self.db.c.execute('''SELECT * from db WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1')))

        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


# Поиск по имени
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app

    def init_search(self):
        # Основные параметры окна
        self.title("Поиск")
        self.geometry("300x100")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        lable_seach = tk.Label(self, text='Поиск')
        lable_seach.place(x=50, y=20)

        # Поле для ввода данных для поиска
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        # Кнопка закрытия окна
        btn_cansel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cansel.place(x=185, y=50)

        # Кнопка поиска
        self.btn_search = ttk.Button(self, text="Поиск")
        self.btn_search.place(x=105, y=50)
        self.btn_search.bind("<Button-1>", lambda event: self.view.search_records(self.entry_search.get()))
        self.btn_search.bind("<Button-1>", lambda event: self.destroy(), add="+")


# Создание базы данных м Функции для работы с ней
class DB:
    # Создание базы данных
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS db (
        id INTEGER NOT NULL PRIMARY KEY,
        name TEXT,
        tel TEXT,
        email TEXT,
        salary REAL);
        """)
        self.conn.commit()

    #Добавлениe данных
    def insert_data(self, name, tel, email, salary):
        self.c.execute("""INSERT INTO db (name, tel, email, salary) VALUES (?, ?, ?, ?)""", (name, tel, email, salary))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    root.title("Телефонная книга")
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()
