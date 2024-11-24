# Test Time Calculator

This repository contains scripts to calculate the total test time from multiple CSV files and the float time (slack) based on the total test time and a given completion or start time.

## Python Script

**test_time_calculator.py**

This Python script calculates the total test time from a set of CSV files in a specified folder. It extracts the "Test Start Time" and "Test End Time" from each file, calculates the time difference, and sums the differences to get the total test time. Additionally, it calculates the float time (slack) based on the total test time and user-provided completion or start time.

**Features**

* Reads CSV files in a specific format where all data is in the first row.
* Extracts "Test Start Time" and "Test End Time" using regular expressions.
* Calculates the total test time from all CSV files.
* Calculates the float time based on the total test time and user-provided completion or start time.
* Formats the output to display individual test times and the total test time.
* Writes the results to a text file named "total_test_time.txt".
* **Exports the results to a CSV file named "test_times.csv" with summary information (Total Test Time, Total Work Time, Float Time) and detailed test times for each file.**

**Usage**

1. Make sure you have Python installed on your system.
2. Save the `test_time_calculator.py` script and the CSV files in the same directory.
3. Open a terminal or command prompt and navigate to the directory.
4. Run the script using the command `python test_time_calculator.py`.
5. The script will prompt you to enter the completion time or start time in `HH:MM:SS` or `HHMM` format.
6. The results will be displayed in the terminal and saved to "total_test_time.txt" and "test_times.csv".

## Batch Script

**start_test_time_calculator.cmd**

This batch script provides a convenient way to run the `test_time_calculator.py` script without having to type the Python command in the terminal.

**Features**

* Checks if the Python script exists.
* Runs the Python script.
* Checks if the Python script executed successfully.
* Checks if the result file exists and is not empty.
* Displays the result.

**Usage**

1. Save the `start_test_time_calculator.cmd` script in the same directory as the Python script.
2. Double-click the `start_test_time_calculator.cmd` file to run the script.
3. The results will be displayed in the command prompt window.

## Author

Starke Wang
