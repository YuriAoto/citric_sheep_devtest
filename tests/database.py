import os
import time
import datetime
import logging

import pytest

import database
import util
import datetime_parser

logging.basicConfig(filename='test_elevator.log',
                    encoding='utf-8',
                    filemode='w',
                    level=logging.DEBUG)

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


@pytest.fixture
def basic_entry():
    return {'floor': 1}


def set_dt(entry):
    entry['plain_dt'] = util.now()


def test_set_reset(db):
    assert db.is_set
    assert os.path.isfile(db.full_database_path)
    db.reset()
    assert not db.is_set


def test_add(db, basic_entry):
    set_dt(basic_entry)
    len_before = len(db)
    db._add(basic_entry)
    assert len(db) == len_before + 1
    last_entry = db.get_all()[-1]
    assert last_entry.floor == basic_entry['floor']
    assert last_entry.plain_dt == basic_entry['plain_dt']
    db.reset()


def test_remove_old_1(db, basic_entry):
    set_dt(basic_entry)
    db._add(basic_entry)
    time.sleep(5)
    set_dt(basic_entry)
    db._add(basic_entry)
    db.remove_old(older_than=datetime.timedelta(seconds=3))
    assert len(db) == 1


def test_remove_old_2(db, basic_entry):
    for _ in range(4):
        time.sleep(4)
        set_dt(basic_entry)
        db._add(basic_entry)
    db.remove_old(older_than=datetime.timedelta(seconds=6))
    assert len(db) == 2


def test_parser(db, dt_parser_hw):
    db.add_parser(dt_parser_hw)
    now = util.now()
    logging.debug('dtparser = %s', db._dt_parser)
    db.add_demand(1, now)
    last_demand = db.get_all()[-1]
    logging.info(f'last demand: %s', last_demand)
    assert 1 == 1

def test_parser_2(db_hw):
    now = util.now()
    logging.debug('dtparser = %s', db_hw._dt_parser)
    db_hw.add_demand(1, now)
    last_demand = db_hw.get_all()[-1]
    logging.info(f'last demand: %s', last_demand)
    assert 1 == 1
