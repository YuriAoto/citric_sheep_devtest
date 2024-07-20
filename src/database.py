"""Class to deal with the database of demands

"""
import os
import logging
import datetime

from sqlalchemy import create_engine, select, delete
from sqlalchemy import DateTime, Integer, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, registry
from sqlalchemy.ext.declarative import declarative_base

from datetime_parser import ParserNotConfiguredError
from util import now


def _demand_table_from_dtparser(D, dt_parser, metadata):
    """Map class D with the content from dt_parser in the SQLAlchemy way
    """
    table_args = ['dtinfo', metadata]
    table_args.append(Column('dtid', Integer, primary_key=True))
    table_args.append(Column('plain_dt', DateTime))
    table_args.append(Column('floor', Integer))
    for col_name, type_, dt_func in dt_parser:
        print(col_name, type_, dt_func)
        table_args.append(Column(col_name, type_))
    return Table(*table_args)

class Base(DeclarativeBase):
    pass

class _Demand:
    def __repr__(self):
        return f'demand(dtid={self.dtid}), floor={self.floor}'


class DemandDatabase:
    """Database for elevator demands
    
    This class wraps all functions to deal with the database.
    
    """
    _databases_dir = 'databases'
    class Demand(_Demand):
        pass

    def __init__(self, dt_parser, filename='elevator.db'):
        self._filename = filename
        self.dt_parser = dt_parser
        self.engine = create_engine(f'sqlite:///{self.full_database_path}')
        demand_table = _demand_table_from_dtparser(self.Demand, dt_parser, Base.metadata)
        Base.metadata.create_all(self.engine)
        self.mapper_registry = registry()
        self.mapper_registry.map_imperatively(self.Demand, demand_table)
        

    @property
    def full_database_path(self):
        return os.path.join(self._databases_dir, self._filename)

    @property
    def is_set(self):
        return os.path.isfile(self.full_database_path)

    def reset(self):
        """Reset the database
        
        This method removes the database file and clears SQLAlchemy internals
        to allow mapping to a new Table
        """
        if self.is_set:
            self.mapper_registry.dispose()
            Base.metadata.clear()
            os.remove(self.full_database_path)

    def __len__(self):
        with Session(self.engine) as session:
            return session.query(self.Demand).count()

    def _add(self, info):
        logging.debug('Adding to database: %s', info)
        with Session(self.engine) as session:
            new_demand = self.Demand(**info)
            session.add(new_demand)
            session.commit()

    def add_demand(self, floor, time):
        """Add a demand to the database"""
        try:
            info = self.dt_parser.parse(time)
            info['floor'] = floor
            self._add(info)
            logging.info('Put demand on database: floor %s at time %s', floor, time)
        except ParserNotConfiguredError:
            logging.warning('Put demand on database failed: parser not configured.')

    def get_all(self):
        logging.debug('Getting all database')
        with Session(self.engine) as session:
            all_demands = select(self.Demand)
            all_demands = [demand for demand in session.scalars(all_demands)]
        return all_demands

    def extract_demands(self):
        """Extract dt demands info and floors from database

        Return:
        -------
        The datetime and floor demands, in separate objects,
        from the db database.
        """
        dt_demands = None
        floors = None
        return dt_demands, floors

    def remove_old(self, older_than):
        """Older than

        Parameters:
        -----------
        older_than (datetime.timedelta)   
        
        """
        logging.debug('Removing older demands from database.')
        cut_off_date = now() - older_than
        sqlalcm_statement = delete(self.Demand).where(self.Demand.plain_dt < cut_off_date)
        with Session(self.engine) as session:
            result = session.execute(sqlalcm_statement)
            session.commit()
        logging.info('Removed %s old entries from database', result.rowcount)
