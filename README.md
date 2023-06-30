### Description ###

This is just an example project to test any API.
It is also include some useful methods which are not used in an example project,
feel free to use it.

Fictitious 'AdminApi' test are placed in AdminApi/test folder. 
Pytest used as a main test runner. 
All test results are get into allure report.

Project can be used in 2 modes

- consistent mode, when tests are going one after another
- load (parallel mode) when threads starts together and make some load on endpoint

### Adding new test

API response validation tests consist of 4 required parts:

- tests, must start with test_
- fixtures, must end with _fixture
- steps, must end with _steps
- models - to validate response data types

### Allure Report

Steps:
- download allure-cli and unzip the archive to any folder
- add a new environment variable:
    - ALLURE_HOME = folder with unpacked archive (root folder)
    - PATH add '%ALLURE_HOME%\bin'
- run tests with the ```"--alluredir=result/allure"```
- generate report by calling ```allure generate result/allure```
- open the report ```allure open```

### LOCUST ###

Before start:
```export PYTHONPATH=PycharmProjects/game_autotests```

terminal command:
```locust --headless --users 1 --spawn-rate 1 -f /pathToProject/game_autotests/LocustLoadTest```

web view mode:
```locust -f /Users/ayzat/PycharmProjects/game_autotests/LocustLoadTest --class-picker```
