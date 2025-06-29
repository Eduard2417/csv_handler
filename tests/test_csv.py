from unittest.mock import patch

import pytest

from csv_handler import get_parse_args, open_csv, Query
from exceptions import FilterError, AggregateError


def test_get_parse_args(get_args):
    assert get_args.file == 'data.csv'
    assert get_args.where == 'age>18'
    assert get_args.aggregate == 'age=min'


def test_open_csv(get_args, get_table, get_header):
    table, header = open_csv(get_args)
    assert table == get_table
    assert header == get_header


def test_aggregate_min(get_args, get_table):
    table, header = Query.aggregate(get_table, get_args)
    assert table == [{'age': 17.0}]
    assert header == ['min']


@pytest.mark.parametrize('args, table_result, header_result', [
    (['script_name', '--file', 'data.csv', '--aggregate', 'age=min'],
     [{'age': 17.0}], ['min']),
    (['script_name', '--file', 'data.csv', '--aggregate', 'age=max'],
     [{'age': 22.0}], ['max']),
    (['script_name', '--file', 'data.csv', '--aggregate', 'age=avg'],
     [{'age': 19.11111111111111}], ['avg']),
])
def test_aggregate(args, table_result, header_result, get_table):
    with patch('sys.argv', args):
        args = get_parse_args()
        table, header = open_csv(args)
        query_table, query_header = Query.aggregate(table, args)
        assert table_result == query_table
        assert header_result == query_header


@pytest.mark.parametrize('args, table_result', [
    (['script_name', '--file', 'data.csv', '--where', 'age=20'],
     [{'name': 'Oleg', 'age': '20', 'command': '1'},
      {'name': 'Ed', 'age': '20', 'command': '3'}]),
    (['script_name', '--file', 'data.csv', '--where', 'age>20'],
     [{'name': 'Gleb', 'age': '21', 'command': '1'},
      {'name': 'Andrey', 'age': '22', 'command': '3'}]),
    (['script_name', '--file', 'data.csv', '--where', 'age<18'],
     [{'name': 'Ilya', 'age': '17', 'command': '1'},
      {'name': 'Artem', 'age': '17', 'command': '3'}]),
])
def test_where(args, table_result):
    with patch('sys.argv', args):
        args = get_parse_args()
        table, header = open_csv(args)
        query_table = Query.where(table, args)
        assert query_table == table_result


@patch('sys.argv',
       ['script_name', '--file', 'data.csv', '--aggregate', 'age=sum'])
def test_aggregate_raise(get_table):
    args = get_parse_args()
    with pytest.raises(AggregateError):
        Query.aggregate(get_table, args)


@patch('sys.argv', ['script_name', '--file', 'data.csv', '--where', 'age+10'])
def test_where_raise(get_table):
    args = get_parse_args()
    with pytest.raises(FilterError):
        Query.where(get_table, args)


def test_where_with_aggregate(get_args, get_table):
    table = Query.where(get_table, get_args)
    table, header = Query.aggregate(table, get_args)
    assert table == [{'age': 19.0}]
    assert header == ['min']
