@ECHO OFF
TITLE Test Time Calculator

REM -------------------------------------------------------------------
REM @description: This script calculates the total test time from all 
REM               CSV files in a given folder.
REM 
REM @author: Starke Wang
REM 
REM @param python_script: The path to the Python script.
REM -------------------------------------------------------------------

REM Clear the screen.
CLS

REM Set the path to the Python script.
SET "python_script=%~dp0test_time_calculator.py"

REM Check if the Python script exists.
IF NOT EXIST "%python_script%" (
  ECHO Error: Python script not found.
  PAUSE
  EXIT /B 1
)

REM Run the Python script.
ECHO Running Python script...
python "%python_script%"

REM Check if the Python script executed successfully.
IF %ERRORLEVEL% NEQ 0 (
  ECHO Error: Python script failed with error code %ERRORLEVEL%.
  PAUSE
  EXIT /B 1
)

REM Check if the result file exists and is not empty.
IF NOT EXIST "total_test_time.txt" (
  ECHO Error: Result file not found.
  PAUSE
  EXIT /B 1
) ELSE (
  FOR %%A IN ("total_test_time.txt") DO IF %%~zA EQU 0 (
    ECHO Error: Result file is empty.
    PAUSE
    EXIT /B 1
  )
)

REM Display the result.
ECHO.
TYPE total_test_time.txt
ECHO.

REM Wait for 5 seconds and then close the window.
TIMEOUT /T 5