import re
from datetime import datetime, timedelta
from pathlib import Path
import csv

def read_file(file_path, encoding='utf-8'):
    """Reads the content of a file.

    Args:
        file_path (Path): The path to the file.
        encoding (str, optional): The encoding of the file. Defaults to 'utf-8'.

    Returns:
        str: The content of the file as a single string.
    """
    with file_path.open('r', encoding=encoding, errors='replace') as f:
        return f.read()


def extract_time_from_string(file_content, pattern):
    """Extracts time information from a string using a regular expression.

    Args:
        file_content (str): The string containing the time information.
        pattern (str): The regex pattern to match the time string.
            The pattern should include a capturing group to extract
            the time information.

    Returns:
        datetime or None: The extracted time information as a datetime object,
                         or None if no match is found.

    Raises:
        re.error: If the given regular expression is invalid.
    """
    try:
        match = re.search(pattern, file_content)
        if match:
            time_str = match.group(1)
            if time_str:  # Check if time_str is not None
                try:
                    return datetime.strptime(time_str.strip(), "%m/%d/%Y %H:%M:%S")
                except ValueError:
                    try:
                        return datetime.strptime(time_str.strip(), "%Y/%m/%d %H:%M:%S")
                    except ValueError:
                        print(f"Unsupported time format in string: {time_str}")
                        return None
            else:
                return None  # Return None if no match is found
        else:
            return None  # Return None if no match is found
    except re.error as e:
        raise re.error(f"Invalid regular expression: {e}")


def extract_time(file_content, time_label):
    """Extracts the time specified by the time_label from the file content.

    Args:
        file_content (str): The content of the file as a single string.
        time_label (str): The label of the time to extract 
                         (e.g., "Test Start Time", "Test End Time").

    Returns:
        datetime or None: The extracted time as a datetime object, 
                         or None if the time could not be extracted.
    """
    # Try matching with both time formats
    patterns = [
        fr"{time_label}:\s*(\d{{2}}/\d{{2}}/\d{{4}} \d{{2}}:\d{{2}}:\d{{2}})",
        fr"{time_label}:\s*(\d{{4}}/\d{{2}}/\d{{2}} \d{{2}}:\d{{2}}:\d{{2}})"
    ]
    for pattern in patterns:
        time_obj = extract_time_from_string(file_content, pattern)
        if time_obj:
            return time_obj

    return None



def extract_test_times(file_path):
    """Extracts "Test Start Time" and "Test End Time" from a CSV file.

    Args:
        file_path (Path): The path to the CSV file.

    Returns:
        tuple: A tuple containing the "Test Start Time" and "Test End Time" as
              datetime objects, or None if an error occurs.
    """
    try:
        file_content = read_file(file_path)
        start_time = extract_time(file_content, "Test Start Time")
        end_time = extract_time(file_content, "Test End Time")
        if start_time is None:
            print(f"Could not find 'Test Start Time' in: {file_path}")
        if end_time is None:
            print(f"Could not find 'Test End Time' in: {file_path}")
        return start_time, end_time
    except (FileNotFoundError, TypeError) as e:
        print(f"Error processing file {file_path}: {e}")
        return None


def calculate_total_test_time(folder_path):
    """Calculates the total test time from all CSV files in a given folder.

    Args:
        folder_path (str): The path to the folder containing the CSV files.

    Returns:
        tuple: A tuple containing the total test time, the number of CSV files
              processed, and a list of tuples with start time, end time, and
              test time for each file.
    """
    total_time = timedelta(0)
    file_count = 0
    test_times = []

    folder_path = Path(folder_path)
    for file_path in folder_path.glob('*.csv'):
        times = extract_test_times(file_path)
        if times:
            start_time, end_time = times
            if start_time is not None and end_time is not None:
                test_time = end_time - start_time
                total_time += test_time
                file_count += 1
                test_times.append((start_time, end_time, test_time, file_path.name))

    return total_time, file_count, test_times


def format_test_times(test_times):
    """Formats the list of test times into a readable string.

    Args:
        test_times (list): A list of tuples with start time, end time, and
                           test time for each file.

    Returns:
        str: A formatted string with the test times.
    """
    # Sort test times by start time in ascending order
    test_times.sort(key=lambda x: x[0])
    output_str = ""
    for i, (start_time, end_time, test_time, filename) in enumerate(test_times):
        formatted_test_time = str(test_time).split()[-1]
        output_str += f"[{i+1}] File: {filename}, Start Time: {start_time.strftime('%H:%M:%S')}, End Time: {end_time.strftime('%H:%M:%S')}, Test Time: {formatted_test_time}\n"
    return output_str


def calculate_float_time(total_test_time, completion_time, start_time):
    """Calculates the float time (slack) based on total test time, completion time, and start time.

    Args:
        total_test_time (timedelta): The total test time.
        completion_time (str): The completion time in HH:MM:SS or HHMM format.
        start_time (str): The start time in HH:MM:SS or HHMM format.

    Returns:
        tuple: A tuple containing the float time and a boolean indicating if the calculation was successful.
    """
    try:
        # Check if completion_time is in HHMM format
        if len(completion_time) == 4:
            completion_time = f"{completion_time[:2]}:{completion_time[2:]}:00"
        completion_time_obj = datetime.strptime(completion_time, "%H:%M:%S")

        # Check if start_time is in HHMM format
        if len(start_time) == 4:
            start_time = f"{start_time[:2]}:{start_time[2:]}:00"
        start_time_obj = datetime.strptime(start_time, "%H:%M:%S")

        # If completion_time is earlier than start_time, assume it's on the next day
        if completion_time_obj.time() < start_time_obj.time():
            completion_time_obj += timedelta(days=1)

        # Calculate total_work_time as the difference between completion_time and start_time
        total_work_time = completion_time_obj - datetime.combine(completion_time_obj.date(), start_time_obj.time())

        # Calculate float_time using total_work_time
        float_time = total_work_time - total_test_time

        return float_time, True
    except ValueError:
        return None, False


def export_to_spreadsheet(test_times, total_test_time, float_time, completion_time, start_time):
    """Exports the test times to a spreadsheet.

    Args:
        test_times (list): A list of tuples with start time, end time, and test time for each file.
        total_test_time (timedelta): The total test time.
        float_time (timedelta): The float time.
        completion_time (str): The completion time.
        start_time (str): The start time.
    """
    try:
        with open('test_times.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Calculate total work time
            total_work_time = timedelta(0)
            if completion_time and start_time:
                float_time, success = calculate_float_time(total_test_time, completion_time, start_time)
                if success:
                    total_work_time = total_test_time + float_time

            # Write summary information first
            writer.writerow(["Total Test Time", total_test_time])
            writer.writerow(["Total Work Time", total_work_time])
            writer.writerow(["Float Time", float_time])
            writer.writerow([])  # Add an empty row to separate summary from details

            # Write the header row for detailed test times
            writer.writerow(["File", "Start Time", "End Time", "Test Time"])

            for start_time, end_time, test_time, filename in test_times:
                writer.writerow([filename, 
                                 start_time.strftime('%Y-%m-%d %H:%M:%S'), 
                                 end_time.strftime('%Y-%m-%d %H:%M:%S'), 
                                 test_time])

        print("Test times exported to test_times.csv")
    except Exception as e:
        print(f"Error exporting to spreadsheet: {e}")



if __name__ == "__main__":
    """
    This script calculates the total test time from all CSV files in a given folder.

    Author: Starke Wang
    """
    import sys

    # Check if a folder path argument is provided.
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        # If no argument is provided, use the default path.
        folder_path = r""

    total_test_time, file_count, test_times = calculate_total_test_time(folder_path)

    # Format the test times string
    test_times_str = format_test_times(test_times)

    # Get completion time or start time from user input
    completion_time = input("Enter completion time in HH:MM:SS or HHMM format (or press Enter to skip): ")
    start_time = input("Enter start time in HH:MM:SS or HHMM format (or press Enter to skip): ")

    # Calculate float time
    float_time, success = calculate_float_time(total_test_time, completion_time, start_time)

    # Write the result to a text file.
    output_file_path = Path("./total_test_time.txt")
    with output_file_path.open("w") as f:
        f.write(f"Total test time: {total_test_time}\n")
        f.write(f"Number of CSV files: {file_count}\n")
        f.write("Individual test times:\n")
        f.write(test_times_str)
        if success:
            f.write(f"Float time: {float_time}\n")

    # Print the result and the path to the output file.
    print(f"Total test time: {total_test_time}")
    print(f"Number of CSV files: {file_count}")
    print("Individual test times:")
    print(test_times_str)
    if success:
        print(f"Float time: {float_time}")
    print(f"Result saved to: {output_file_path.absolute()}")

    # Export to spreadsheet
    export_to_spreadsheet(test_times, total_test_time, float_time, completion_time, start_time)
