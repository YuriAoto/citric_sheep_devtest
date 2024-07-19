"""A elevator model to predict the best resting position

Citric Sheep Tech Test

Yuri Alexandre Aoto

"""

import logging
import asyncio

import elevator_model, datetime_parser, database, system_ctrl

logging.basicConfig(filename='elevator.log',
                    encoding='utf-8',
                    filemode='w',
                    level=logging.DEBUG)


async def main():
    """Main function that creates objects and gather the coroutine objects"""
    dt_parser = datetime_parser.DateTimeParser()
    dt_parser.set('The parser')
    db = database.DemandDatabase(dt_parser)
    elevator = elevator_model.Elevator(db)
    await asyncio.gather(system_ctrl.run_elevator(elevator),
                         system_ctrl.make_ml_training(elevator))

if __name__ == '__main__':
    asyncio.run(main())
    logging.info('Done!')
