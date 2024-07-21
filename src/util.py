import sys
import traceback
import logging
import datetime

def traceback_exception(msg):
    """Return a string with 'msg' and the exception traceback."""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_msg = msg + ':\n'
    tb_msg += "  Value: " + str(exc_value) + "\n"
    tb_msg += "  Type:  " + str(exc_type) + "\n"
    tb_msg += "  Traceback:\n"
    for tb in traceback.extract_tb(exc_traceback):
        tb_msg += "    in {0}, line {1:d}: {2}, {3}\n".format(tb[0],
                                                             tb[1],
                                                             str(tb[2]),
                                                             tb[3])
    return tb_msg


def now():
    """Return current datetime
    
    This is a direct call to datetime.datetime.now
    Alternatively, timezone.utc could be passed,
    but this seems not to be stored in sqlite,
    leading to failed tests when comparing datetimes
    before and after storing in the database.
    
    """
    return datetime.datetime.now()

def parse_configfile(filename):
    """Return information from config file
    
    Parameters:
    -----------
    filename (str) the filename; see format below
    
    Return:
    -------
    dt_parser_list, ml_when, older_than
    
    where:
        dt_parser_list:  list that can be used to create a DateTimeParser object
        ml_when: Information about when the ML training should happen
        older_than: a datetime.deltatime object; database older than this should be removed
    
    Example:
    ------------
    The following example illustrates the file format. If the file contains:
    
    hour
    week day
    make ml traning at : 
    remove database entries older than : 2 days
    
    Then the following is returned
    
    ['hour', 'week day'], 
    
    """
    ml_when = datetime.timedelta(seconds=5)
    older_than = datetime.timedelta(seconds=10)
    dt_parser_list = []
    with open(filename) as f:
        for line in f:
            line = line.split('#')[0]
            if ':' in line:
                k, v = tuple(map(lambda x: x.strip(), line.split(':')))
                logging.debug('Parsing line: key=%s with value=%s, from line\n:%s',
                              k, v, line)
                if k == 'ML traning at each':
                    ml_when = _parse_deltatime(v)
                elif k == 'remove demands older than':
                    older_than = _parse_deltatime(v)
                else:
                    raise ValueError('Configure file is not correct at this line:\n%s',
                                     line)
            else:
                dt_parser_list.append(line.strip())
                logging.debug('Parsing line: new entry in parser list: %s', dt_parser_list[-1])
    logging.debug('Parsing config file results:\n'
                  'parser list: %s\n'
                  'ml_when: %s\n'
                  'older_than: %s\n',
                  dt_parser_list, ml_when, older_than
                  )
    return dt_parser_list, ml_when, older_than


def _parse_deltatime(dt_str):
    """Return a deltatime from string.
    
    Parameters:
    -----------
    dt_str (str) the deltatime as a string
    
    Examples:
    ---------
    >>> _parse_deltatime("5 days")
    datetime.timedelta(days=5)
    >>> _parse_deltatime("2 weeks")
    datetime.timedelta(days=14)
    >>> _parse_deltatime("4 weeks, 4 days")
    datetime.timedelta(days=32)
    
    Possible things to use are the same as the arguments
    to create datetime.timedelta
    """
    kw_dict = {}
    for dt_entry in dt_str.split(','):
        v, k = dt_entry.split()
        kw_dict[k.strip()] = int(v)
    return datetime.timedelta(**kw_dict)
