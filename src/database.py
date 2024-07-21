"""Class to deal with the database of demands

"""
import os
import logging
import datetime

import pandas as pd

from sqlalchemy import create_engine, select, delete, literal_column
from sqlalchemy import DateTime, Integer, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, registry
from sqlalchemy.ext.declarative import declarative_base

import datetime_parser
from util import now


def _demand_table_from_dtparser(D, dt_parser, metadata):
    """Map class D with the content from dt_parser in the SQLAlchemy way
    """
    table_args = ['dtinfo', metadata]
    table_args.append(Column('dtid', Integer, primary_key=True))
    table_args.append(Column('plain_dt', DateTime))
    table_args.append(Column('floor', Integer))
    for col_name, type_, dt_func in dt_parser:
        table_args.append(Column(col_name, type_))
    return Table(*table_args)

class Base(DeclarativeBase):
    pass

class _Demand:
    def __repr__(self):
        return f'demand (id={self.dtid}) at floor={self.floor}'

def _get_dt_parser(dt_parser):
    if isinstance(dt_parser, datetime_parser.DateTimeParser):
        return dt_parser
    if isinstance(dt_parser, str):
        return datetime_parser.DateTimeParser.from_file(dt_parser)
    if isinstance(dt_parser, list):
        return datetime_parser.DateTimeParser.from_list(dt_parser)
    if dt_parser is None:
        return datetime_parser.DateTimeParser()

class DemandDatabase:
    """Database for elevator demands
    
    This class wraps all functions to deal with the database.
    
    """
    _databases_dir = 'databases'
    class Demand(_Demand):
        pass

    def __init__(self,
                 dt_parser=None,
                 filename='elevator.db',
                 remove_old_db=False):
        self._filename = filename
        self.engine = None
        self.mapper_registry = None
        self._dt_parser = _get_dt_parser(dt_parser)
        self.set_sqlalchemy_map(remove_old_db=remove_old_db)

    @property
    def dt_parser(self):
        return self._dt_parser

    def add_parser(self, dt_parser):
        self._dt_parser = dt_parser
        self.set_sqlalchemy_map()

    def set_sqlalchemy_map(self, remove_old_db=False):
        self.reset(remove_old_db=remove_old_db)
        self.engine = create_engine(f'sqlite:///{self.full_database_path}')
        demand_table = _demand_table_from_dtparser(self.Demand,
                                                   self.dt_parser,
                                                   Base.metadata)
        logging.debug('demand_table: %r', demand_table)
        Base.metadata.create_all(self.engine)
        self.mapper_registry = registry()
        self.mapper_registry.map_imperatively(self.Demand, demand_table)

    @property
    def full_database_path(self):
        return os.path.join(self._databases_dir, self._filename)

    @property
    def is_set(self):
        return self.engine is not None

    @property
    def file_exists(self):
        return os.path.isfile(self.full_database_path)

    def reset(self, remove_old_db=True):
        """Reset the database
        
        This method removes the database file and clears SQLAlchemy internals
        to allow mapping to a new Table
        """
        if self.is_set:
            self.mapper_registry.dispose()
            Base.metadata.clear()
        if remove_old_db and self.file_exists:
            os.rename(self.full_database_path,
                      f'{self.full_database_path}_{now().strftime("%Y%m%d%H%M%S%f")}')
        self.engine = None
        self.mapper_registry = None

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
        except datetime_parser.ParserNotConfiguredError:
            logging.warning('Put demand on database failed: parser not configured.')

    def get_all(self):
        logging.debug('Getting all database')
        with Session(self.engine) as session:
            all_demands = select(self.Demand)
            all_demands = [demand for demand in session.scalars(all_demands)]
        return all_demands

    def get_all_pandas(self):
        logging.debug('Getting all into pandas df')
        return  pd.read_sql_query(select(self.Demand), self.engine)
    
    def get_full_str(self):
        all_demands = self.get_all()
        return '\n'.join([(repr(d) + ': '
                           + ', '.join([f'{n}={d.__dict__[n]}' for n,_,_ in self.dt_parser])
                           )
                           for d in self.get_all()])

    def extract_demands(self):
        """Extract dt demands info and floors from database

        Return:
        -------
        The datetime and floor demands, in separate objects,
        from the db database.
        """
        floors = pd.read_sql_query(select(self.Demand.floor),
                                   self.engine)['floor']
        dt_demands = pd.read_sql_query(select(*[self.Demand.__dict__[n]
                                                for n,_,_ in self.dt_parser]),
                                       self.engine)
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

