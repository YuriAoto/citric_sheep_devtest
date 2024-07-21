"""A elevator model to predict the best resting position

Citric Sheep Tech Test

Yuri Alexandre Aoto

"""
import logging
import asyncio

from database import DemandDatabase
from util import parse_configfile
from elevator_model import Elevator
from system_ctrl import run_elevator, make_ml_training, clean_older_entries

logging.basicConfig(filename='elevator.log',
                    encoding='utf-8',
                    filemode='w',
                    level=logging.DEBUG)

config_file = 'elevator_config.txt'

async def main():
    """Main function that creates objects and gather the coroutine objects"""
    dt_parser_list, ml_when, older_than = parse_configfile(config_file)
    db = DemandDatabase(dt_parser=dt_parser_list,
                        force_new_database=False)
    logging.debug('Current database:\n %s', db.get_full_str())
    elevator = Elevator(db)
    await asyncio.gather(run_elevator(elevator),
                         make_ml_training(elevator, ml_when),
                         clean_older_entries(db, older_than))

if __name__ == '__main__':
    asyncio.run(main())
    logging.info('Done!')
