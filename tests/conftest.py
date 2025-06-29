from unittest.mock import patch

import pytest

from csv_handler import get_parse_args


@pytest.fixture
@patch('sys.argv',
       ['script_name', '--file', 'data.csv', '--where',
        'age>18', '--aggregate', 'age=min'])
def get_args():
    return get_parse_args()


@pytest.fixture
def get_table():
    return [
        {'name': 'Oleg', 'age': '20', 'command': '1'},
        {'name': 'Gleb', 'age': '21', 'command': '1'},
        {'name': 'Ilya', 'age': '17', 'command': '1'},
        {'name': 'Dima', 'age': '18', 'command': '2'},
        {'name': 'Arthur', 'age': '18', 'command': '2'},
        {'name': 'Lena', 'age': '19', 'command': '2'},
        {'name': 'Ed', 'age': '20', 'command': '3'},
        {'name': 'Andrey', 'age': '22', 'command': '3'},
        {'name': 'Artem', 'age': '17', 'command': '3'}
    ]


@pytest.fixture
def get_header():
    return ['name', 'age', 'command']
