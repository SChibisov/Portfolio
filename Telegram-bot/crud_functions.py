import sqlite3

connection_products = sqlite3.connect('Products.db')
cursor_products = connection_products.cursor()

cursor_products.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    );
    ''')
cursor_products.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                        ('Продукт1', 'Описание1', 'Цена: 100'))

cursor_products.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                        ('Продукт2', 'Описание2', 'Цена: 200'))

cursor_products.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                        ('Продукт3', 'Описание3', 'Цена: 300'))

cursor_products.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                        ('Продукт4', 'Описание4', 'Цена: 400'))

connection_products.commit()
connection_products.close()


def initiate_db():
    connection_users = sqlite3.connect('Users.db')
    cursor_users = connection_users.cursor()
    cursor_users.execute('''
            CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL, 
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL
            )
            ''')
    connection_users.commit()


initiate_db()


def get_all_products():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    products = cursor.execute('SELECT * FROM Products').fetchall()
    connection.commit()
    return products


def add_user(username, email, age, balance='1000'):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (username, email, age, balance))
    connection.commit()


def is_included(username):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    verify_users = cursor.execute(f'SELECT username FROM Users WHERE username=?',
                                  (username,)).fetchone()
    if verify_users is None:
        return False
    else:
        connection.commit()
        return True
