import os
from pytest import fixture
import pmb_py
from pmb_py import log_in, log_out

@fixture()
def pmb():
    log_in(os.environ['PMBUSER'], os.environ['PMBPW'])
    yield pmb_py
    log_out()