import importlib.resources
import os

import pytest
from plotmanx import resources

from ..analyze.pri import LogFile


@pytest.fixture(name='logfile_path')
def logfile_fixture(tmp_path):
    log_name = '2021-05-07T20_25_52.851358+08_00.log'
    log_contents = importlib.resources.read_binary(resources, log_name)
    log_file_path = tmp_path.joinpath(log_name)
    log_file_path.write_bytes(log_contents)
    return log_file_path


def test_one():
    log_name = '2021-05-07T20_25_52.851358+08_00.log'
    dir = '/Users/hesdx/Documents/ipfs/plotman/src/plotmanx/_tests/resources'
    file = os.path.join(dir, log_name)
    fileo = LogFile(file)
    fileo.init_logfile()
    fileo.print()


test_one()
