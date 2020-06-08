import hashlib
import math
import socket
import subprocess
import sys

from cloudpickle import dumps, loads

BUFF = 1024 * 10

HOST = '192.168.1.181'
PORT = 8888


def assert_equal(expected, recived):
    return type(expected) == type(recived) and expected == recived


def send_func(func, args, exec_type, commands_dict=None):
    """Функция отправки, сериализации и получения результата"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer_dict = {
        'func': func,
        'args': args,
        'exec_type': exec_type,
        'commands': commands_dict
    }
    transfer_data = dumps(transfer_dict)
    s.connect((HOST, PORT))
    s.send(transfer_data)
    result_data = s.recv(BUFF)
    result = loads(result_data)
    print(f"Accepted data: {result}")
    return result


def create_file(data: bytes):
    with open('tmp_file.txt', 'wb') as f:
        f.write(data)
    with open('tmp_file.txt', 'rb') as f:
        hashsum = hashlib.md5(f.read()).hexdigest()
    return hashsum


def factorial1(num):
    """Расчет факториала от числа 1000 и возврат строки с последним числом и размером числа в байтах"""
    f = 1
    for i in range(1, num + 1):
        f *= i
    return f'last_num: {f % 10} ,factorial_size: {f.__sizeof__()}'


def install_req(package):
    """Установка модуля из скрипта, импорт этого модуля (не стандартый импорт), возврат версии этого модуля"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    exec(f'import {package}')
    res = eval(f'{package}.__version__')
    return res


def inside_import():
    """Функиця импортирует (стандартый импорт) модуль requests и возвращает версию"""
    import requests
    return requests.__version__


def test_request(url):
    """Отправка запроса Get запроса по URL и возврат статуса ответа и заголовков"""
    import requests
    r = requests.get(url)
    return r.status_code, r.headers


def inner_call_another():
    """Вызов пользовательской функции внутри другой функции"""
    return factorial1(5)


def factorial_without_inside_import(num):
    """Вызов функции факториала без явного импорта модуля math"""
    return math.factorial(num)


def postgres_connection(credentials_dict, sql_list, table_name):
    """Работа с базой данных Postgresql, переданы доступы на подключение, список sql команд, имя таблицы,
    функиця создает таблицу, заполняет данными и возвращает результат"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'psycopg2-binary'])
    import psycopg2
    connection = psycopg2.connect(**credentials_dict)
    cursor = connection.cursor()
    for sql in sql_list:
        cursor.execute(sql.format(table_name))
    res = cursor.fetchall()
    cursor.execute(f'drop table {table_name};')
    return res


def test_case(func, args, test_name, description=None):
    print('-' * 10)
    print(f'Имя теста: {test_name}')
    if description:
        print(f'Описание теста: {description}')
    elif func.__doc__:
        print(f'Описание теста: {func.__doc__}')
    print('-' * 10)
    local_result = func(*args)
    remote_result = send_func(func, args, 'PROCESS').get('result')[0]
    print(f'Полученные результаты совпадают?: {assert_equal(local_result, remote_result)}')
    print(f"\nlocal_result:  {local_result}")
    print(f'remote_result: {remote_result}')
    print('-' * 10)
    print(test_name, "Закончен!")
    print('-' * 10)
    print()


TEST_CASES = (
    (factorial1, (1000,), 'Расчет факториала числа 1000',),
    (
        create_file, (b'test data for hashing',), 'Создание файла и подсчет хэш суммы этого файла',
        'Создает файл tmp.txt, записывает в него переданные данные и возвращает хэш сумму'
    ),
    (
        install_req, ('requests',), 'Установка requests и получение версии модуля'
    ),
    (
        inside_import, (), 'Стандратный импорт предустановленной библиотеки'
    ),
    (
        test_request, ('http://atpp.vstu.edu.ru/avt/',), 'Отправка запроса на сайт кафедры АВТ'
    ),
    (
        inner_call_another, (), 'Вызов внутри функции'
    ),
    (
        factorial_without_inside_import, (3,), 'Вызов функции факториала из math',
    ),
    (
        postgres_connection,
        ({'dbname': 'postgres', 'user': 'postgres', 'password': 'toor', 'host': '192.168.1.181'},
         ['create table {} ( id bigserial primary key, txt varchar(20));',
          "insert into {} values(0,'qwe0');",
          "insert into {} values(1,'qwe1');",
          "insert into {} values(2,'qwe2');",
          'select * from {};'], 'testng3'
         ), 'Работа с базой данных Postgresql'

    ),
)

if __name__ == '__main__':
    print('Start Correctness Testing')
    for case in TEST_CASES:
        if case:
            test_case(*case)
