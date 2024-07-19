"""Define the coroutines that will control the application"""
import asyncio
import logging

import ml_prediction
import database

async def run_elevator(elevator):
    """Run the elevator, waiting for demands"""
    logging.info('Starting elevator.')
    for i in range(10):
        logging.info('A demand')
        elevator.demand(i)
        await asyncio.sleep(1)


async def make_ml_training(elevator):
    """Make ML training at specified times"""
    for i in range(2):
        logging.info('Making ML training')
        mlp = ml_prediction.create_predictor_from_db(*elevator.db.extract_demands())
        elevator.mlp = mlp
        await asyncio.sleep(4)


async def clean_older_entries(db, older_than):
    """Remove older entries of database at regular times"""
    for i in range(1):
        logging.info('Remiving older entries from database')
        db.remove_old(older_than)
        await asyncio.sleep(8)

