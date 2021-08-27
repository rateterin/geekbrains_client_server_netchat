"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""


import chardet
import subprocess


sub_proc = subprocess.Popen(('ping', 'yandex.ru'), stdout=subprocess.PIPE)
for line in sub_proc.stdout:
    print(line.decode(encoding=chardet.detect(line)['encoding']))
