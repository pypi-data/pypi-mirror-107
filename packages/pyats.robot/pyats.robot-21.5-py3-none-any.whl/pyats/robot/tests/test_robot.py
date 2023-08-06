#!/usr/bin/env python

import inspect
import unittest
import shutil
import sys, os, re
from unittest.mock import Mock, patch, MagicMock, call
import tempfile
import subprocess

from pyats.topology.testbed import Testbed
from pyats.results import Passed, Failed, Errored, Aborted
from pyats.easypy.tasks import TaskManager
from pyats.robot.runner import run_robot
from robot.libraries.BuiltIn import BuiltIn
from robot.errors import PassExecution, DATA_ERROR, STOPPED_BY_USER,\
                         FRAMEWORK_ERROR
from robot.run import RobotFramework

multiprocessing = __import__('multiprocessing').get_context('fork')


class Test_Robot_Script(unittest.TestCase):

    def setUp(self):
        self.logsdir = tempfile.mkdtemp(prefix='robot')

    def tearDown(self):
        shutil.rmtree(self.logsdir)

    def test_robot(self):
        pwd = os.path.dirname(__file__)
        env = os.environ.copy()
        env['PYTHONPATH'] = ':'.join([pwd, env.get('PYTHONPATH', '')])

        output = []
        with subprocess.Popen('robot -d %s pyats.robot' % self.logsdir,
                              shell=True,
                              cwd = pwd,
                              env = env,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as p:
            for line in p.stdout:
                line = line.decode('utf-8')
                print(line, end='') # interactive display
                output += line

        self.assertEqual(p.returncode, 3)

        expected = '''
==============================================================================
Pyats
==============================================================================
Initialize                                                            | PASS |
------------------------------------------------------------------------------
CommonSetup                                                           | PASS |
common_setup has passed
------------------------------------------------------------------------------
Testcase1 pass                                                        | PASS |
tc_one has passed
------------------------------------------------------------------------------
Testcase1 fail                                                        [ ERROR ] Failed reason: failed
| FAIL |
tc_one_failed has failed
------------------------------------------------------------------------------
Testcase1 aborted                                                     [ ERROR ] Aborted reason: aborted
| FAIL |
tc_one_aborted has aborted
------------------------------------------------------------------------------
Testcase1 errored                                                     [ ERROR ] Errored reason: errored
| FAIL |
tc_one_errored has errored
------------------------------------------------------------------------------
Testcase1 skipped                                                     | PASS |
tc_one_skipped has skipped
------------------------------------------------------------------------------
Testcase1 blocked                                                     | PASS |
tc_one_blocked has blocked
------------------------------------------------------------------------------
Pyats                                                                 | FAIL |
8 tests, 5 passed, 3 failed
        '''

        output = ''.join(output).rstrip()
        for line in expected.splitlines():
            self.assertIn(line, output)



class Test_RobotFramework(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from pyats.robot.pyATSRobot import pyATSRobot
        cls.py = pyATSRobot()
        #cls.unicon_mock = MagicMock()
        #modules = {'unicon' : cls.unicon_mock}
        #cls.module_patcher = patch.dict('sys.modules', modules)
        #cls.module_patcher.start()

    @classmethod
    def tearDown(cls):
        pass
        #cls.module_patcher.stop()

    def test_init(self):
        from pyats.robot.pyATSRobot import pyATSRobot
        global pyATSRobot
        py = pyATSRobot()
        self.assertIs(py.datafile, None)
        self.assertIsInstance(py.builtin, BuiltIn)

    def test_load_testbed(self):
        testbed = Testbed('tb')
        py = pyATSRobot()
        testbed = os.path.join( os.path.dirname(__file__), 'testbed-myconn.yaml')

        self.assertIs(py.testbed, None)
        py.use_testbed(testbed)
        self.assertIsInstance(py.testbed, Testbed)

    def test_run_passing_testcase(self):
        py = pyATSRobot()
        m = Mock()
        m.side_effect = PassExecution('Pass')
        py.builtin.pass_execution = m
        with self.assertRaises(PassExecution):
            py.run_testcase('basic_example_script.tc_no_argument')

    def test_run_failing_testcase(self):
        py = pyATSRobot()
        m = Mock()
        m.side_effect = AssertionError('failed')
        py.builtin.fail = m

        with self.assertRaises(AssertionError):
            py.run_testcase('basic_example_script.tc_no_argument_fail')

    def test_run_testcase_datafile(self):
        py = pyATSRobot()
        testbed = os.path.join( os.path.dirname(__file__), 'testbed-myconn.yaml')
        py.use_testbed(testbed)

        py.datafile = 'datafile.yaml'
        m = Mock()
        m.side_effect = PassExecution('Pass')
        py.builtin.pass_execution = m
        with self.assertRaises(PassExecution):
            py.run_testcase('basic_example_script.common_setup')

        m.side_effect = AssertionError('failed')
        py.builtin.fail = m
        with self.assertRaises(AssertionError):
            py.run_testcase('basic_example_script.tc_one_failed')

    def test_connect_to_device_kwargs(self):
        testbed = """
        devices:
          host:
            os: linux
            type: host
            connections:
              cli:
                command: bash
        """
        self.py.use_testbed(testbed)
        dev = self.py.testbed.devices.host
        dev.connect = Mock()
        self.py.connect_to_device_kwargs(device='host', init_exec_commands=[])
        dev.connect.assert_has_calls([call(init_exec_commands=[])])


class Test_Robot_Task(unittest.TestCase):
    def setUp(self):
        self.runinfo_dir = tempfile.mkdtemp(prefix='runinfo_dir')
        self.mock_runtime = Mock()
        self.mock_runtime.directory = self.runinfo_dir
        self.mock_runtime.job.rerun_dict = None
        self.mock_runtime.job.testbed = None
        self.mock_runtime.plugins.has_errors.return_value = False
        self.mock_runtime.synchro = multiprocessing.Manager()
        self.mock_runtime.tasks = TaskManager(runtime = self.mock_runtime)

    def tearDown(self):

        self.mock_runtime = None
        shutil.rmtree(self.runinfo_dir)

    def test_robot_success(self):
        with patch.object(RobotFramework, 'execute') as mock_execute:
            mock_execute.return_value = 0
            robot_result = run_robot(robotscript = 'somescript.robot', runtime = self.mock_runtime)
            self.assertEqual(robot_result, Passed)
            self.assertEqual(self.mock_runtime.tasks.result, Passed)

    def test_robot_failure(self):
        with patch.object(RobotFramework, 'execute') as mock_execute:
            mock_execute.return_value = 33
            robot_result = run_robot(robotscript = 'somescript.robot', runtime = self.mock_runtime)
            self.assertEqual(robot_result, Failed)
            self.assertEqual(self.mock_runtime.tasks.result, Failed)

    def test_robot_error(self):
        with patch.object(RobotFramework, 'execute') as mock_execute:
            mock_execute.return_value = DATA_ERROR
            robot_result = run_robot(robotscript = 'somescript.robot', runtime = self.mock_runtime)
            self.assertEqual(robot_result, Errored)
            self.assertEqual(self.mock_runtime.tasks.result, Errored)

    def test_robot_abort(self):
        with patch.object(RobotFramework, 'execute') as mock_execute:
            mock_execute.return_value = STOPPED_BY_USER
            robot_result = run_robot(robotscript = 'somescript.robot', runtime = self.mock_runtime)
            self.assertEqual(robot_result, Aborted)
            self.assertEqual(self.mock_runtime.tasks.result, Aborted)


class Test_Easypy_Robot_Runner(unittest.TestCase):

    def setUp(self):
        self.runinfo_dir = tempfile.mkdtemp(prefix='runinfo_dir')
        pwd = os.path.dirname(__file__)
        env = os.environ.copy()
        env['PYTHONPATH'] = ':'.join([pwd, env.get('PYTHONPATH', '')])
        self.env = env

    def tearDown(self):
        shutil.rmtree(self.runinfo_dir)

    def test_run_easypy(self):
        job = os.path.join(os.path.dirname(__file__), 'robot_job.py')

        p = subprocess.Popen(['easypy', job, '-runinfo_dir', self.runinfo_dir,
                              '-no_archive', '-no_mail', '-testbed_file',
                              'testbed-myconn.yaml'],
                             stdout = subprocess.PIPE,
                             env = self.env,
                             universal_newlines = True)
        p.wait()

        out = p.stdout.read()

        expected = '''
Task-1: hello_world.Should Pass                                           PASSED
Task-1: hello_world.Should Fail                                           FAILED
Task-1: hello_world.Logging Test                                          PASSED
Task-1: hello_world.Check Testbed Provided                                PASSED
'''.strip().splitlines()
        for i, line in enumerate(out.splitlines()):
            if expected[0] in line:
                for expected, l in zip(expected, out.splitlines()[i:i+4]):
                    self.assertIn(expected, l)
                break
        else:
            raise Exception('Did not get expected output!!!')

        match = re.search(r'%EASYPY-INFO: Runinfo directory: (.+)', out)
        runinfo = match.groups()[0]

        self.assertIn(os.path.join(runinfo, 'Task-1.robot/output.xml'),
                      out)
        self.assertIn(os.path.join(runinfo, 'Task-1.robot/report.html'),
                      out)
        self.assertIn(os.path.join(runinfo, 'Task-1.robot/log.html'),
                      out)

    def test_double_run_easypy(self):
        job = os.path.join(os.path.dirname(__file__), 'robot_double_job.py')

        p = subprocess.Popen(['easypy', job, '-runinfo_dir', self.runinfo_dir,
                              '-no_archive', '-no_mail', '-testbed_file',
                              'testbed-myconn.yaml'],
                             stdout = subprocess.PIPE,
                             env = self.env,
                             universal_newlines = True)
        p.wait()

        out = p.stdout.read()

        expected = '''
Task-1: hello_world.Should Pass                                           PASSED
Task-1: hello_world.Should Fail                                           FAILED
Task-1: hello_world.Logging Test                                          PASSED
Task-1: hello_world.Check Testbed Provided                                PASSED
Task-2: hello_world.Should Pass                                           PASSED
Task-2: hello_world.Should Fail                                           FAILED
Task-2: hello_world.Logging Test                                          PASSED
Task-2: hello_world.Check Testbed Provided                                PASSED
'''.strip().splitlines()
        for i, line in enumerate(out.splitlines()):
            if expected[0] in line:
                for expected, l in zip(expected, out.splitlines()[i:i+4]):
                    self.assertIn(expected, l)
                break
        else:
            raise Exception('Did not get expected output!!!')

        match = re.search(r'%EASYPY-INFO: Runinfo directory: (.+)', out)
        runinfo = match.groups()[0]

        self.assertIn(os.path.join(runinfo, 'Task-1.robot/output.xml'),
                      out)
        self.assertIn(os.path.join(runinfo, 'Task-1.robot/report.html'),
                      out)
        self.assertIn(os.path.join(runinfo, 'Task-1.robot/log.html'),
                      out)
        self.assertIn(os.path.join(runinfo, 'Task-2.robot/output.xml'),
                      out)
        self.assertIn(os.path.join(runinfo, 'Task-2.robot/report.html'),
                      out)
        self.assertIn(os.path.join(runinfo, 'Task-2.robot/log.html'),
                      out)

    def test_run_pyats_run_robot(self):
        robot = os.path.join(os.path.dirname(__file__), 'hello_world.robot')

        p = subprocess.Popen(['pyats', 'run', 'robot', robot,
                              '--runinfo-dir', self.runinfo_dir,
                              '--no-archive', '--no-mail', '--testbed-file',
                              'testbed-myconn.yaml'],
                             stdout = subprocess.PIPE,
                             env = self.env,
                             universal_newlines = True)
        p.wait()

        out = p.stdout.read()

        expected = '''
Task-1: hello_world.Should Pass                                           PASSED
Task-1: hello_world.Should Fail                                           FAILED
Task-1: hello_world.Logging Test                                          PASSED
Task-1: hello_world.Check Testbed Provided                                PASSED
'''.strip().splitlines()
        for i, line in enumerate(out.splitlines()):
            if expected[0] in line:
                for expected, l in zip(expected, out.splitlines()[i:i+4]):
                    self.assertIn(expected, l)
                break
        else:
            raise Exception('Did not get expected output!!!')

        match = re.search(r'%EASYPY-INFO: Runinfo directory: (.+)', out)
        runinfo = match.groups()[0]

        self.assertIn(os.path.join(runinfo, 'Task-1.robot/output.xml'),
                      out)
        self.assertIn(os.path.join(runinfo, 'Task-1.robot/report.html'),
                      out)
        self.assertIn(os.path.join(runinfo, 'Task-1.robot/log.html'),
                      out)


if __name__ == '__main__': # pragma: no cover
    unittest.main()
