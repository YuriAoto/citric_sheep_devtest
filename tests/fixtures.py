import logging

import pytest

import datetime_parser
import database


@pytest.fixture
def db():
    new_db = database.DemandDatabase(filename='test_database.db')
    logging.info('Created new database for fixture')
    yield new_db
    new_db.reset()

@pytest.fixture
def dt_parser_hw():
    parser = datetime_parser.DateTimeParser()
    parser.set_new_col('hour')
    parser.set_new_col('week day')
    logging.debug(f'Parser hw: %r', parser)
    yield parser

@pytest.fixture
def db_hw(dt_parser_hw):
    new_db = database.DemandDatabase(dt_parser=dt_parser_hw, filename='test_database.db')
    logging.info('Created new database for fixture')
    yield new_db
    new_db.reset()
