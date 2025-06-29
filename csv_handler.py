import argparse
import csv
import re

import tabulate

from exceptions import FilterError, AggregateError


def get_parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки.

    Returns:
        argparse.Namespace: Парсенные аргументы командной строки.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str,
                        help='csv-file path',
                        required=True)
    parser.add_argument('--where', type=str,
                        help='filtering by field',
                        required=False)
    parser.add_argument('--aggregate', type=str,
                        help='performing an aggregate function',
                        required=False)
    return parser.parse_args()


class Aggregate:
    """Класс для выполнения агрегатных функций."""

    @staticmethod
    def min(table: list, param: str) -> float:
        """Находит минимальное значение указанного параметра.

        Args:
            table (list): Список словарей, представляющих строки таблицы.
            param (str): Название параметра для поиска минимума.

        Returns:
            float: Минимальное значение параметра.
        """
        return min([float(line[param]) for line in table])

    @staticmethod
    def max(table: list, param: str) -> float:
        """Находит максимальное значение указанного параметра.

        Args:
            table (list): Список словарей, представляющих строки таблицы.
            param (str): Название параметра для поиска максимума.

        Returns:
            float: Максимальное значение параметра.
        """
        return max([float(line[param]) for line in table])

    @staticmethod
    def avg(table: list, param: str) -> float:
        """Находит среднее значение указанного параметра.

        Args:
            table (list): Список словарей, представляющих строки таблицы.
            param (str): Название параметра для вычисления среднего.

        Returns:
            float: Среднее значение параметра.
        """
        value_list = [float(line[param]) for line in table]
        return sum(value_list) / len(value_list)


class Query:
    """Класс для выполнения запросов к таблице данных."""

    @staticmethod
    def where(table: list, args: argparse.Namespace) -> list:
        """Фильтрует строки таблицы по заданному условию.

        Args:
            table (list): Список словарей, представляющих строки таблицы.
            args (argparse.Namespace): Аргументы командной строки,
            содержащие условие фильтрации.

        Returns:
            list: Отфильтрованный список строк.

        Raises:
            FilterError: Если оператор не корректен.
        """

        operator_match = re.search(r'[=<>]', args.where)

        if operator_match is None:
            raise FilterError('Введите корректный оператор')

        operator = operator_match.group(0)

        param, value = re.split(r'[=<>]', args.where)

        if operator == '=':
            return [line for line in table if line[param] == value]
        elif operator == '<':
            return [line for line in table if line[param] < value]
        elif operator == '>':
            return [line for line in table if line[param] > value]
        else:
            raise FilterError('Введите корректный оператор')

    @staticmethod
    def aggregate(table: list, args: argparse.Namespace) -> tuple:
        """Выполняет агрегатную функцию для заданного параметра.

        Args:
            table (list): Список словарей, представляющих строки таблицы.
            args (argparse.Namespace): Аргументы командной строки,
            содержащие условие агрегирования.

        Returns:
            tuple: Словарь с результатом агрегатной функции и
            список с её названием.

        Raises:
            AggregateError: Если функция не существует.
        """
        param, value = args.aggregate.split('=')
        if value == 'min':
            return [{param: Aggregate.min(table, param)}], [value]
        elif value == 'max':
            return [{param: Aggregate.max(table, param)}], [value]
        elif value == 'avg':
            return [{param: Aggregate.avg(table, param)}], [value]
        else:
            raise AggregateError(f'Функция {value} не существует')


def open_csv(args: argparse.Namespace) -> tuple:
    """Открывает CSV файл и считывает данные в виде списков словарей.

    Args:
        args (argparse.Namespace): Аргументы командной строки,
        содержащие путь к файлу.

    Returns:
        tuple: Список словарей с данными и список заголовков.
    """
    with open(args.file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames
        return list(reader), header


def main(args: argparse.Namespace) -> None:
    """Основная функция, выполняющая логику программы.

    Args:
        args (argparse.Namespace): Аргументы командной строки.
    """
    table, header = open_csv(args)

    if args.where:
        table = Query.where(table, args)

    if args.aggregate:
        table, header = Query.aggregate(table, args)

    for field in range(len(table)):
        table[field] = list(table[field].values())

    print(tabulate.tabulate(table, headers=header, tablefmt='outline'))


if __name__ == '__main__':
    args = get_parse_args()
    main(args)
