"""Define the coroutines that will control the application"""
import sys
import asyncio
import logging
import traceback
from datetime import datetime

import ml_prediction
import database
from util import now, traceback_exception

_socket_name = '.elevator_connection.unix.socket'


def _decode_message(msg):
    floor, dt = msg.decode().strip().split()
    try:
        floor = int(floor)
    except ValueError:
        pass
    dt = datetime.fromisoformat(dt)
    logging.debug('Decoded message: floor = %s, datetime = %s', floor, dt)
    return floor, dt

async def _elevator_demand_send_message(writer, floor, dt):
    logging.debug('Sending message: floor=%s ; dt=%s', floor, dt)
    msg_bytes = (f'{floor} {dt.isoformat()}\n').encode()
    writer.write(msg_bytes)
    await writer.drain()
 
async def _elevator_demand_read_response(reader):
    logging.debug('Elevator demand: Waiting for response...')
    result_bytes = await reader.readline()
    response = result_bytes.decode()
    logging.debug('Received response: %s,', response.strip())
    try:
        prediction = int(response)
    except ValueError:
        prediction = None
    return prediction

def _elevator_interaction(floor, dt, elevator):
    """Send a demand or ask the prediction to the elevator."""
    if isinstance(floor, int):
        elevator.demand(floor, dt=dt)
        msg_back = f'Demand received\n'.encode()
    else:
        predicted_floor = elevator.predict_best_resting_floor(dt)
        msg_back = f'{predicted_floor}\n'.encode()
    return msg_back

async def _handle_demands(reader, writer, elevator):
    msg_bytes = await reader.readline()
    try:
        floor, dt = _decode_message(msg_bytes)
    except Exception as e:
        logging.error('When decoding message: %s', e)
    logging.debug('Request %s, at %s', floor, dt)
    try:
        msg_back = _elevator_interaction(floor, dt, elevator)
    except Exception as e:
        logging.error('When decoding message: %s', e)
    logging.debug('We will send now this message back: %s', msg_back)
    writer.write(msg_back)
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    logging.debug('Closing connection')


async def elevator_demand_main(floor, dt):
    """Main function to make a elevator demand.
    
    This function is supposed to be called from elevator_demand.py
    
    Parameters:
    -----------
    floor (int) the floor
    dt (datetime.datetime) the datetime of the demand
    
    """
    logging.debug('Elevator demand: connecting to %s ...', _socket_name)
    reader, writer = await asyncio.open_unix_connection(_socket_name)
    logging.debug('Elevator demand: connected')
    await _elevator_demand_send_message(writer, floor, dt)
    prediction = await _elevator_demand_read_response(reader)
    logging.debug('Elevator demand: Shutting down connection.')
    writer.close()
    await writer.wait_closed()
    return prediction

async def run_elevator(elevator):
    """Run the elevator, waiting for demands from unix socket"""
    elevator_server = await asyncio.start_unix_server(
        lambda r, w: _handle_demands(r, w, elevator),
        _socket_name)
    async with elevator_server:
        logging.info('Elevator server has started.')
        await elevator_server.serve_forever()

async def make_ml_training(elevator, wait_for):
    """Make ML training at specified times
    
    Parameters:
    -----------
    wait_for (datetime.timedelta)
        How long do we wait for the next training.
    
    """
    while True:
        await asyncio.sleep(wait_for.total_seconds())
        logging.info('Making ML training')
        try:
            all_demands = elevator.db.extract_demands()
            logging.debug('All demands: datetimes:\n%s', all_demands[0])
            logging.debug('All demands: floors:\n%s', all_demands[1])
            mlp = ml_prediction.training(*all_demands)
        except ml_prediction.MLPredictionError:
            ex_type, ex, tb = sys.exc_info()
            logging.error(traceback_exception(
                'Error at the ML training. Skipping making new training this time'))
        else:
            elevator.mlp = mlp


async def clean_older_entries(db, older_than, wait_for=0.1):
    """Remove older entries of database at regular times
    
    Remove older entries from the database at regular time periods.
    
    Parameters:
    -----------
    older_than (datetime.timedelta)
        Entries are removed if older than this
    wait_for (float or datetime.timedelta)
        How long do we wail until next cleaning.
        If float, we consider wait_for*older_than
    
    """
    if isinstance(wait_for, float):
        wait_for = older_than * wait_for
    while True:
        await asyncio.sleep(wait_for.total_seconds())
        logging.info('Removing older entries from database')
        db.remove_old(older_than)
