import re
import unicodedata

before = []
after = []
between = []
equal = []
dollars_marker = 10000 # Если значение зарпралты 10000 или менее значит зарплата указана в долларах.

def clean_digits(myline, selector):
    digits =  myline.split(' ') # Разделяем строку ['до/от', '20\u202f000', 'руб.\n'] и оставляем толко чистую цифру и валюту
    if selector == 'beforeafter':
        digits_wospaces =  re.sub('\s+', '', digits[1]) # Удаляем пробелы между разрядами.
        currency = re.sub('\n', '', digits[2])
    elif selector == 'between':
        digits_wospaces =  re.sub('\s+', '', digits[1]) # Удаляем пробелы между разрядами.
        currency = re.sub('\n', '', digits[2]) # Данную функцию можно переписать, указав только if для between, тогда во всех остальных будет beforeafter

    return digits_wospaces


def if_before_match(myline):
    """
    Если значение зарплаты указано как например "до 60 000 руб." Создаем список из встреченных в файле строк
    """
    if re.match(r'до', myline):
        myline = clean_digits(myline, selector='beforeafter')
        # print(myline)
        before.append(myline)
    return before

def if_after_match(myline):
    """
    Если значение зарплаты указано как например "от 60 000 руб." Создаем список из встреченных в файле строк
    """
    if re.match(r'от', myline):
        myline = clean_digits(myline, selector='beforeafter')
        after.append(myline)
    return after

def if_between_match(myline):
    """
    Если значение зарплаты указано как например "60 000  - 100 000 руб." Создаем список из встреченных в файле строк. В формате:
    ['before', 'after', 'currency']
    """
    if re.search(r'–', myline):
        between.append(myline)
    return between





def parse_between(between_match):
    """
    На вход получаем списко полученный из строк "60 000  - 100 000 руб." Создаем список без пробелов и лишних символов
    ['от', 'до', 'валюта']
    
    """
    first_digit_list = []
    second_digit_list = []
    currency_list = []
    for el in between_match:
        spliting_digits = el.split('–')
        first_digit = re.sub('\s+', '', spliting_digits[0])
        if int(first_digit) / 100 < 1:
            first_digit = int(first_digit) * 1000
        second_digit_raw = spliting_digits[1].split(' ')
        second_digit = re.sub('\s+', '', second_digit_raw[1])
        currency = re.sub('\s', '', second_digit_raw[2])
        first_digit_list.append(first_digit)
        second_digit_list.append(second_digit)
        currency_list.append(currency)
    return [first_digit_list, second_digit_list, currency_list]

def create_date(raw_digits):
    index = 0
    data_dict = {}
    for el in raw_digits:
        stack_currency = []
        number = clean_digits(el[0]).encode('ascii', 'ignore').decode('utf8')+el[1] #Удаляем последовательность UNICODE, добавляем разряд
        index += 1
        stack_currency.append(number)
        stack_currency.append(el[2])
        data_dict[index] = stack_currency
    return data_dict


myfile = open("the_salary.txt", encoding='utf8')
while True:
    myline = myfile.readline()
    before_result = if_before_match(myline)
    after_result = if_after_match(myline)
    between_match = if_between_match(myline)
    if not myline:
        break

myfile.close()

between_carrency = parse_between(between_match)

midle_sum = 0
minimum = 100000000
maximum = 0

for index in range(len(between_carrency[0])):
    midle = (int(between_carrency[0][index]) + int(between_carrency[1][index])) / 2
    midle_sum = midle + midle_sum
    if int(between_carrency[0][index]) < minimum:
        minimum = int(between_carrency[0][index])

    if int(between_carrency[1][index]) > maximum:
        maximum = int(between_carrency[1][index])

average_between = midle_sum / len(between_carrency[0])

print(f"Выборка с HH.RU по 140 вакансиям, работодатели которых, указали зарплату\n\
Выборка проводилась по запросу - 'Инженер Технической поддержки'\n")
print('-' * 100)
print(f'Если работодатель указал дапазон зарплат:\n\
Минимальная зарплата: {minimum} рублей\n\
Максимальная зарплата: {maximum} рублей\n\
Средняя зарплата: {average_between} рублей')

print('-' * 100)
"""
Считаем среднее из максимального предложения
"""
accumulator = 0 

for el in before_result:
    if int(el) < dollars_marker:
        el = int(el) * 75 # Учитываем случай если зарплата указывается в долларах
    accumulator = int(el) + accumulator
    avarage_max = accumulator / len(before_result)

print(f'Если работатадель указал зарплтату "ДО", то среднее значение: {avarage_max} рублей')

for el in after_result:
    if int(el) < dollars_marker:
        el = int(el) * 75 # Учитываем случай если зарплата указывается в долларах
    accumulator = int(el) + accumulator
    avarage_min = accumulator / len(after_result)
    avarage_min = round(avarage_min, 2)

print('-' * 100)
print(f'Если работатадель указал минимальную зарплату, то среднее значение: {avarage_min} рублей')