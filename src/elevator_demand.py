#!/usr/bin/env python
import sys
import asyncio
import logging
from datetime import datetime

from system_ctrl import elevator_demand_main
from util import now

logging.basicConfig(filename='elevator_demand.log',
                    encoding='utf-8',
                    filemode='a',
                    level=logging.DEBUG)

if __name__ == '__main__':
    try:
        floor = int(sys.argv[1])
    except ValueError:
        sys.exit('Please, pass the floor (integer) as first argument')
    if len(sys.argv) == 3:
        try:
            dt = datetime.fromisoformat(sys.argv[2])
        except ValueError:
            sys.exit('Date time incorrectly formatted')
    else:
        dt = now()
    asyncio.run(elevator_demand_main(floor, dt))
