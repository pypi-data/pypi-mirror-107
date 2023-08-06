# Demonstration of Robot Framework with pyATS

# Executing any pyATS Testcase within RobotFramework

*** Settings ***
# Importing test libraries, resource files and variable files.

Library        pyats.robot.pyATSRobot

*** Variables ***
# Defining variables that can be used elsewhere in the test data.
# Can also be driven as dash argument at runtime

${datafile}     datafile.yaml
${testbed}      testbed-myconn.yaml

*** Test Cases ***
# Creating test cases from available keywords.

Initialize
    # Initializes the pyATS Testbed
    # pyATS Testbed can be used within pyATS and RASTA
    use testbed "${testbed}"
    connect to device "ios_mock" as alias "cli"

CommonSetup
    # Call any pyATS Testcase
    run testcase "basic_example_script.common_setup"

# Example of calling pyATS Testcase which return different results
Testcase1 pass
    run testcase "basic_example_script.tc_one"
Testcase1 fail
    run testcase "basic_example_script.tc_one_failed"
Testcase1 aborted
    run testcase "basic_example_script.tc_one_aborted"
Testcase1 errored
    run testcase "basic_example_script.tc_one_errored"
Testcase1 skipped
    run testcase "basic_example_script.tc_one_skipped"
Testcase1 blocked
    run testcase "basic_example_script.tc_one_blocked"
