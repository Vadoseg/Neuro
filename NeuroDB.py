import sqlite3  # Библиотека для создания базы данных
import pandas as pd  # Библиотека для работы с данными и БД
from pandas.core.frame import DataFrame  # Используется для вывода таблицы с данными
from sqlalchemy import create_engine  # create_engine предоставляет подключение к БД
import numpy as np  # Требуется для использования np.int64, что тоже самое, как big int
import matplotlib.pyplot as plt  # Библиотека для графиков
import tkinter as tk  # Библиотека для графического интерфейса
from tkinter import messagebox  # Для всплывающих\оповещающих окон
from tkinter.simpledialog import askstring  # Для вызова окон ввода
import os
from pathlib import Path  # Для удобного указания пути к файлам(Переписать код под этот метод)

DB_NAME = "Neuro.db"


def what_os():
    global Path_to_DB
    global engine
    if os.name == "posix":
        for root, dirs, files in os.walk("/home"):
            for file in files:
                if file == DB_NAME:
                    Path_to_DB = os.path.join(root, file)  # Символ r(raw) - Обозначает необработанную строку,
                    # требуется, чтобы символ \ воспринимался, не как escape-символ
                    engine = create_engine(f'sqlite:///{Path_to_DB}')  # Подключаемся к БД

    elif os.name == "nt":
        for root, dirs, files in os.walk(r"C:\Users\Vados\Desktop"):
            for file in files:
                if file == DB_NAME:
                    Path_to_DB = os.path.join(root, file)
                    engine = create_engine(f'sqlite:///{Path_to_DB}')  # Подключаемся к БД
                    print(engine)


def import_files():  # Функция загрузки множества файлов за раз посредством ввода пути до файла

    method = askstring('Введите', 'Загрузить файлы по одному(1), Загрузить все файлы из папки(2):')
    table_name = askstring('Введите', 'Введите название таблицы:')
    if (method == '1'):

        number_of_files = askstring('Введите ', 'Введите кол-во файлов, которое хотите загрузить:')
        number_of_files = int(number_of_files)  # Функция askstring получает значение и передает его в виде str

        if (number_of_files >= 1):
            for i in range(0, number_of_files):
                path_to_csv = askstring('Укажите ', 'Пожалуйста, укажите путь до .csv файла: ')
                get_files(path_to_csv, table_name)

            messagebox.showwarning("ЗАГРУЗКА ДАННЫХ ЗАВЕРШЕНА", "БАЗА ДАННЫХ ПОПОЛНЕНА")
        else:
            messagebox.showwarning("Ошибка Нуля", "Введите число больше 0")  # Загнать в блок ошибок
    else:
        Directory = askstring('Введите', 'Полный путь до папки с файлами')

        start = [get_files(f, table_name) for f in
                 Path(Directory).glob("*.csv")]  # Рекурсивный вызов функции для каждого файла .csv в папке

        messagebox.showwarning("ЗАГРУЗКА ДАННЫХ ЗАВЕРШЕНА", "БАЗА ДАННЫХ ПОПОЛНЕНА")


def get_data():  # Функция вывода всех данных из БД

    conn = sqlite3.connect(Path_to_DB)
    cursor = conn.cursor()

    table_name = askstring('Введите', 'Введите название таблицы:')
    cursor.execute("SELECT * FROM %s ORDER BY id ASC" % table_name)  # Вызов всех данных из таблицы
    rows = cursor.fetchall()  # fetchall() извлекает все данные из последнего выполненого запроса и возвращает в виде списка

    df = DataFrame(rows)
    df.columns = ['id', 'Type', 'Level',
                  'Miliseconds']  # Задаём названия столбцам для понятного вывода, иначе пронумерует столбцы

    print()
    print(table_name)
    print(df.to_string(index=False, header=True,
                       justify='left'))  # Выводит таблицу по левому краю, преобразует все данные в строку, чтобы можно было вывести
    print()

    conn.commit()
    cursor.close()
    conn.close()


def graf():  # Функция вывода графика

    X4 = []
    Y4 = []  # Координаты для Type 4

    X5 = []
    Y5 = []  # Координаты для Type 5

    conn = sqlite3.connect(Path_to_DB)
    cursor = conn.cursor()

    number = []
    number = askstring('Введите', 'Введите строки, столбцы и кол-во графиков через пробел:')

    number = number.split()  # Разбивает строку на массив строчных элементов

    number = list(map(int,
                      number))  # Функция map применяет функцию int к каждому элементу итерируемого списка, а затем функция list преобразует это в список

    # if (number[0]*number[1] < number[2]): Создать блок ошибок
    # print("ERROR, please try again")
    # graf()

    for i in range(1, number[2] + 1):
        table_name = askstring('Введите', 'Введите название таблицы:')

        queryX4 = "SELECT id FROM %s WHERE Type = 4 AND Level > 0 AND Level < 200" % table_name  # Создаем выборку id для Type 4
        cursor.execute(queryX4)  # Выполняем выборку
        results1 = cursor.fetchall()  # Записываем в переменную все данные

        queryY4 = "SELECT Level FROM %s WHERE Level > 0 AND Type = 4 AND Level < 200" % table_name  # Создаем выборку Level для Type 4
        cursor.execute(queryY4)
        results2 = cursor.fetchall()

        queryX5 = "SELECT id FROM %s WHERE Type = 5 AND Level > 0 AND Level < 200" % table_name  # Создаем выборку id для Type 5
        cursor.execute(queryX5)
        results3 = cursor.fetchall()

        queryY5 = "SELECT Level FROM %s WHERE Level > 0 AND Type = 5 AND Level < 200" % table_name  # Создаем выборку Level для Type 5
        cursor.execute(queryY5)
        results4 = cursor.fetchall()

        X4 = list(results1)
        Y4 = list(results2)

        X5 = list(results3)
        Y5 = list(results4)

        # Упростил код, заменил громоздкий код на функцию list
        # for results1 in results1:     #Записываем все данные из выборок в переменную-список
        # X4.append(results1[0])

        plt.subplot(number[0], number[1], i)
        plt.plot(X4, Y4)  # Создаем оба графика
        plt.plot(X5, Y5)

        plt.title('График')  # Название графика
        plt.xlabel('id')  # Подпись оси Х
        plt.ylabel('LEVEL')  # Подпись оси Y
        plt.legend(['Концентрация', 'Медитация'])  # Легенда графика

    plt.show()
    cursor.close()
    conn.close()


def get_files(file_name, table_name):
    # Вызываем функцию каждый раз для каждого файла csv в папке указанной в Path
    df = pd.read_csv(file_name)  # Читает файл .csv

    new_df = df['_id,"type","level","miliseconds"'].str.split(',', expand=True)  # Разбиваем основной столбец на 4
    new_df.columns = ['id', 'Type', 'Level', 'Miliseconds']  # Даем название столбцам

    new_df = new_df.replace(to_replace='"', value='',
                            regex=True)  # Команда убирает лишние ковычки для дальнейшего преобразования текста в числа
    new_df = new_df.astype(
        np.int64)  # Преобразуем текст из файла в числа, также благодаря этому при загрузке файлов в БД столбцы обретут тип данных BIGINT

    new_df.to_sql(table_name, con=engine, if_exists='append', index=False)  # Импортирует данные в таблицу БД


what_os()
window = tk.Tk()

window.resizable(width=False, height=False)
window.geometry('720x360')

window.title('Neuro Data Base')

Welcome = tk.Label(window, text='Выберите действие', font=('Arial Bold', 18), fg='black')
Welcome.pack(anchor='center', pady=30)

Button_1 = tk.Button(window, text='Пополнить Базу Данных', command=import_files, width='30', height='1', fg='black',
                     bg='gray', font=('Arial', 14))
Button_1.pack(anchor='center', pady=20)

Button_2 = tk.Button(window, text='Вывести Базу Данных', command=get_data, width='30', height='1', fg='black',
                     bg='gray', font=('Arial', 14))
Button_2.pack(anchor='center', pady=20)

Button_3 = tk.Button(window, text='Вывести график', command=graf, width='30', height='1', fg='black', bg='gray',
                     font=('Arial', 14))
Button_3.pack(anchor='center', pady=20)

window.mainloop()

# Проблема с линиями в графиках из-за того, что прибор в calm и stressed снимал значения с одинаковым id

# Написать блок ошибок(Желательно в отдельном файле)
# Оптимизация кода:
# Numba Just In Time (Jit) Плохо работает со строками, но ускоряет вычисления. Также в нём есть Parallel(Разбивает процессы функций на разные потоки)
# PyPy интрепретатор, хорошо работает со строками(Имеет свой JIT, поэтому особого смысла в Numba нет)

