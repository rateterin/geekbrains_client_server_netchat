"""
Задание 1.

Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить
в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл; Проверить работу
программы через вызов функции write_to_csv().
"""

import os
import chardet
import re
from csv import writer as csv_writer


def get_data(files: tuple = None, fields: tuple = None) -> list or None:
    if not files or not fields:
        raise AttributeError(
            'Оба атрибута обязательны!\r\nfiles - кортеж из имен файлов,\r\nfields - кортеж полей для выборки.')
    data = ''
    result_lists = [[field for field in fields]]
    for n, file in enumerate(files, 1):
        if not os.path.exists(file):
            print(f'Файл не найден: {file}')
            return None
        with open(file, 'rb') as in_f:
            buff = in_f.read(10240)
            while buff:
                data = buff
                buff = in_f.read(10240)
            data = data.decode(chardet.detect(data).get('encoding'))
            result_lists.append([])
            for field in fields:
                match = re.search(f'{field}:.+', data).group()
                result_lists[n].append(re.split(r':\s+', match)[1].removesuffix('\r').strip())
    return result_lists


def write_to_csv(csv_file: str = None):
    if csv_file:
        with open(csv_file, 'w', encoding='utf-8') as out_f:
            f_writer = csv_writer(out_f)
            for row in get_data(files=('info_1.txt', 'info_2.txt', 'info_3.txt'),
                                fields=('Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы')):
                f_writer.writerow(row)


test_file = os.path.join(os.path.realpath(os.path.curdir), 'test_csv_for_task_1.csv')
write_to_csv(test_file)

with open(test_file, 'r', encoding='utf-8') as test_f:
    print(test_f.read())
