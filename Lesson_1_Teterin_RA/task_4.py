"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

words = ('разработка', 'администрирование', 'protocol', 'standard')
for word in words:
    print(f'Исходное слово: {word}')
    word_enc = word.encode('utf8')
    print(f'encode: {word_enc}')
    word_dec = word_enc.decode('utf8')
    print(f'decode: {word_dec}')
