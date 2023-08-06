import logging

logger = logging.getLogger(__name__)

def hello_world():
   print("HELLO WORLD!")

def raise_exception():
    raise Exception

def do_logging():
    logger.info('test info')
    logger.error('test error')

def check_testbed():
    import os
    assert os.environ['TESTBED'].endswith('testbed-myconn.yaml')
