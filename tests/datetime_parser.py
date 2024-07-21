import datetime

import pytest
from sqlalchemy import Integer

import util
import datetime_parser
from .fixtures import *

def test_empty_parser():
    parser = datetime_parser.DateTimeParser()
    assert not parser._names
    assert not parser._types
    assert not parser._funcs

def test_iter():
    parser = datetime_parser.DateTimeParser()
    parser._names = ['A', 'B', 'C']
    parser._types = ['a', 'b', 'c']
    parser._funcs = [1, 2, 3]
    names = []
    types = []
    funcs = []
    for n,t,f in parser:
        names.append(n)
        types.append(t)
        funcs.append(f)
    assert names == parser._names
    assert types == parser._types
    assert funcs == parser._funcs
    names = []
    types = []
    funcs = []
    for n,t,f in parser:
        names.append(n)
        types.append(t)
        funcs.append(f)
    assert names == parser._names
    assert types == parser._types
    assert funcs == parser._funcs

def test_set_new_col_inner():
    parser = datetime_parser.DateTimeParser()
    parser._set_new_col_inner('A', 'a', 1)
    assert parser._names == ['A']
    assert parser._types == ['a']
    assert parser._funcs == [1]
    parser._set_new_col_inner('B', 'b', 2)
    assert parser._names == ['A', 'B']
    assert parser._types == ['a', 'b']
    assert parser._funcs == [1, 2]

@pytest.fixture
def datetime_2024_7_19__2_5():
    return datetime.datetime(2024, 7, 19, hour=2, minute=5)

@pytest.fixture
def datetime_1986_6_7__17_35():
    return datetime.datetime(1986, 6, 7, hour=17, minute=35)

def test_set_new_col_inner(datetime_2024_7_19__2_5,
                           datetime_1986_6_7__17_35):
    parser = datetime_parser.DateTimeParser()

    parser.set_new_col('hour')
    assert parser._names[-1] == 'hour'
    assert parser._types[-1] == Integer
    assert parser._funcs[-1](datetime_2024_7_19__2_5) == 2
    assert parser._funcs[-1](datetime_1986_6_7__17_35) == 17

    parser.set_new_col('month')
    assert parser._names[-1] == 'month'
    assert parser._types[-1] == Integer
    assert parser._funcs[-1](datetime_2024_7_19__2_5) == 7
    assert parser._funcs[-1](datetime_1986_6_7__17_35) == 6

    parser.set_new_col('week day')
    assert parser._names[-1] == 'week day'
    assert parser._types[-1] == Integer
    assert parser._funcs[-1](datetime_2024_7_19__2_5) == 4
    assert parser._funcs[-1](datetime_1986_6_7__17_35) == 5


def test_parse(dt_parser_hw):
    parsed_date = dt_parser_hw.parse_list(datetime.datetime(2024, 7, 1, hour=1))
    logging.debug('parsed date: %s', parsed_date)
    assert parsed_date == [1, 0]
