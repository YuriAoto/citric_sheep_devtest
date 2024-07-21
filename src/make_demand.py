#!/usr/bin/env python
"""Interacts with the elevator, making demands or asking a prediction

Usage:
make_demand.py <floor> [<datetime>]

If <floor> is an integer, a demand is made
If <floor> is the string 'predict',
   returns the prediction for the best resting floor

<datetime> is a string with the datetime in the isoformat
If not passed, use current datetime

"""
import sys
import asyncio
import logging
from datetime import datetime

from system_ctrl import elevator_demand_main
from util import now

logging.basicConfig(filename='demands.log',
                    encoding='utf-8',
                    filemode='a',
                    level=logging.DEBUG)

if __name__ == '__main__':
    try:
        floor = sys.argv[1]
    except ValueError:
        sys.exit('Please, pass at least one argument: the floor or "predict"')
    if len(sys.argv) == 3:
        try:
            dt = datetime.fromisoformat(sys.argv[2])
        except ValueError:
            sys.exit('Date time incorrectly formatted')
    else:
        dt = now()
    prediction = asyncio.run(elevator_demand_main(floor, dt))
    if prediction is not None:
        print(f'Predicted best resting floor: {prediction}')
