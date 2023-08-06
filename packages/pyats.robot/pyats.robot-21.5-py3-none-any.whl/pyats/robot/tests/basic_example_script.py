#!/bin/env python
###################################################################
# basic_example.py : A very simple test script example which include:
#     common_setup
#     Tescases
#     common_cleanup
# The purpose of this sample test script is to show the "hello world"
# of aetest.
###################################################################

# To get a logger for the script
import logging

# Needed for aetest script
from pyats import aetest

# Get your logger for your script
log = logging.getLogger(__name__)

###################################################################
###                  COMMON SETUP SECTION                       ###
###################################################################

# This is how to create a CommonSetup
# You can have one of no CommonSetup
# CommonSetup can be named whatever you want

class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    # CommonSetup have subsection.
    # You can have 1 to as many subsection as wanted
    # here is an example of 2 subsections

    # First subsection
    @aetest.subsection
    def sample_subsection_1(self, testbed, extra_args=None):
        """ Common Setup subsection """
        testbed.devices['ios_mock'].connect()
        log.info("Aetest Common Setup ")

    # If you want to get the name of current section,
    # add section to the argument of the function.

    # Second subsection
    @aetest.subsection
    def sample_subsection_2(self, section, cc_param_a, steps):
        """ Common Setup subsection """
        log.info("Inside %s" % (section))
        log.info("Inside %s" % (cc_param_a))
        self.parent.parameters['fff'] = 5
        with steps.start('bla') as step:
            step.passed('bla')
        self.skipped('ww')

        # And how to access the class itself ?

        # self refers to the instance of that class, and remains consistent
        # throughout the execution of that container.
        log.info("Inside class %s" % (self.uid))

###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

# This is how to create a testcase
# You can have 0 to as many testcase as wanted
@aetest.processors.noreport
def bla2(section):
    log.info('wow2')

@aetest.processors.noreport
def post(section):
    log.info('after')

global_processors = {
    'pre': [bla2,],
    'post': [post,],
}

def blabla(section):
    log.info('wow')

# Testcase name : tc_one
class tc_one(aetest.Testcase):
    """ This is user Testcases section """

    # Testcases are divided into 3 sections
    # Setup, Test and Cleanup.

    # This is how to create a setup section
    @aetest.setup
    def prepare_testcase(self, section, fff, testbed):
        """ Testcase Setup section """
        log.info("Preparing the test")
        log.info(fff)
        log.info(section)

    # This is how to create a test section
    # You can have 0 to as many test section as wanted

    # First test section
    @ aetest.test
    @aetest.processors(pre=[blabla])
    def simple_test_1(self):
        """ Sample test section. Only print """
        log.info("First test section ")

    # Second test section
    @ aetest.test
    def simple_test_2(self):
        """ Sample test section. Only print """
        log.info("Second test section ")

    # This is how to create a cleanup section
    @aetest.cleanup
    def clean_testcase(self):
        """ Testcase cleanup section """
        log.info("Pass testcase cleanup")

# Testcase name : tc_one
class tc_one_failed(aetest.Testcase):
    """ This is user Testcases section """

    # Testcases are divided into 3 sections
    # Setup, Test and Cleanup.

    # This is how to create a setup section
    @aetest.setup
    def prepare_testcase(self, section, testbed, fff):
        """ Testcase Setup section """
        log.info("Preparing the test")
        log.info(fff)
        log.info(section)
        self.failed('failed')
# Testcase name : tc_one
class tc_one_errored(aetest.Testcase):
    """ This is user Testcases section """

    # Testcases are divided into 3 sections
    # Setup, Test and Cleanup.

    # This is how to create a setup section
    @aetest.setup
    def prepare_testcase(self, section, testbed, fff):
        """ Testcase Setup section """
        log.info("Preparing the test")
        log.info(fff)
        log.info(section)
        self.errored('errored')
# Testcase name : tc_one
class tc_one_aborted(aetest.Testcase):
    """ This is user Testcases section """

    # Testcases are divided into 3 sections
    # Setup, Test and Cleanup.

    # This is how to create a setup section
    @aetest.setup
    def prepare_testcase(self, section, testbed, fff):
        """ Testcase Setup section """
        log.info("Preparing the test")
        log.info(fff)
        log.info(section)
        self.aborted('aborted')
# Testcase name : tc_one
class tc_one_skipped(aetest.Testcase):
    """ This is user Testcases section """

    # Testcases are divided into 3 sections
    # Setup, Test and Cleanup.

    # This is how to create a setup section
    @aetest.setup
    def prepare_testcase(self, section, testbed, fff):
        """ Testcase Setup section """
        log.info("Preparing the test")
        log.info(fff)
        log.info(section)
        self.skipped('skipped')
# Testcase name : tc_one
class tc_one_blocked(aetest.Testcase):
    """ This is user Testcases section """

    # Testcases are divided into 3 sections
    # Setup, Test and Cleanup.

    # This is how to create a setup section
    @aetest.setup
    def prepare_testcase(self, section, testbed, fff):
        """ Testcase Setup section """
        log.info("Preparing the test")
        log.info(fff)
        log.info(section)
        self.blocked('blocked')

class tc_one_passx(aetest.Testcase):
    """ This is user Testcases section """

    # Testcases are divided into 3 sections
    # Setup, Test and Cleanup.

    # This is how to create a setup section
    @aetest.setup
    def prepare_testcase(self, section, testbed, fff):
        """ Testcase Setup section """
        log.info("Preparing the test")
        log.info(fff)
        log.info(section)
        self.passx('passx')

class tc_no_argument(aetest.Testcase):
    @aetest.setup
    def prepare_testcase(self, section):
        """ Testcase Setup section """
        log.info("Preparing the test")
        log.info(section)

class tc_no_argument_fail(aetest.Testcase):
    @aetest.setup
    def prepare_testcase(self, section):
        """ Testcase Setup section """
        log.info("Preparing the test")
        log.info(section)
        self.failed('Failed')

#####################################################################
####                       COMMON CLEANUP SECTION                 ###
#####################################################################

# This is how to create a CommonCleanup
# You can have 0 , or 1 CommonCleanup.
# CommonCleanup can be named whatever you want :)
class common_cleanup(aetest.CommonCleanup):
    """ Common Cleanup for Sample Test """

    # CommonCleanup follow exactly the same rule as CommonSetup regarding
    # subsection
    # You can have 1 to as many subsection as wanted
    # here is an example of 1 subsections

    @aetest.subsection
    def clean_everything(self):
        """ Common Cleanup Subsection """
        log.info("Aetest Common Cleanup ")

if __name__ == '__main__': # pragma: no cover
    aetest.main()
