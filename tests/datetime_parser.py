import pytest

import util
import datetime_parser

def test_empty_parser():
    parser = datetime_parser.DateTimeParser()
    assert parser._parserinfo == None
    dt = util.now()
    with pytest.raises(datetime_parser.ParserNotConfiguredError):
        parser.parse(dt)
