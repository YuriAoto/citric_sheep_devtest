import os
import time
import datetime
import logging

import pytest

import database
import util

from .fixtures import *

logging.basicConfig(filename='test_elevator.log',
                    encoding='utf-8',
                    filemode='w',
                    level=logging.DEBUG)


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


def test_parser_2(db_hw):
    now = util.now()
    logging.debug('dtparser = %s', db_hw._dt_parser)
    db_hw.add_demand(1, now)
    last_demand = db_hw.get_all()[-1]
    logging.info(f'last demand: %s', last_demand)
    assert 1 == 1

def test_extract_demands(db_hw):
    db_hw.add_demand(3, datetime.datetime(2024, 7, 21, hour=1))
    db_hw.add_demand(1, datetime.datetime(2024, 7, 21, hour=3))
    db_hw.add_demand(2, datetime.datetime(2024, 7, 21, hour=7))
    dt_demands, floors = db_hw.extract_demands()
    logging.debug('floors:\n%s', floors)
    logging.debug('dt_demands:\n%s', dt_demands)
    assert floors.iloc[0] == 3
    assert floors.iloc[1] == 1
    assert floors.iloc[2] == 2
    assert dt_demands['hour'].iloc[0] == 1
    assert dt_demands['hour'].iloc[1] == 3
    assert dt_demands['hour'].iloc[2] == 7
