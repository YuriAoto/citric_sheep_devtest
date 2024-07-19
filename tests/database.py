import os
import time
import datetime
import logging

import pytest

import database
import util

logging.basicConfig(filename='test_elevator.log',
                    encoding='utf-8',
                    filemode='w',
                    level=logging.DEBUG)

@pytest.fixture
def db():
    new_db = database.DemandDatabase(None, filename='test_database.db')
    yield new_db
    new_db.reset()
    
@pytest.fixture
def basic_entry():
    return {'floor': 1,
            'hour': 1,
            'week_day': 1,
            'month': 1,
            }

def set_dt(entry):
    entry['plain_dt'] = util.now()


def test_set_reset(db):
    assert db.is_set
    assert os.path.isfile(db.full_database_path)
    db.reset()
    assert not db.is_set
    assert not os.path.isfile(db.full_database_path)


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
