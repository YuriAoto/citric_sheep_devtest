from datetime import datetime

import numpy as np

import ml_prediction
from .fixtures import *

def test_extract_demands(db_hw):
    for hour in range(4):
        for day in range(1,3):
            db_hw.add_demand(1, datetime(2024, 7, day, hour=1))
    mlp = ml_prediction.training(*db_hw.extract_demands())
    assert ml_prediction.predict(mlp,
                                 db_hw.dt_parser,
                                 datetime(2024, 7, 1, hour=1)) == 1


