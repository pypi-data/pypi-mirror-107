*** Settings ***
Library         hello_world.py

*** Test Cases ***
Should Pass
    Hello World

Should Fail
    Raise Exception

Logging Test
    Do Logging

Check Testbed Provided
    Check Testbed
