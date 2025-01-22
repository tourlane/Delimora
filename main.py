import os
import csv

folder_path = r"C:\Users\LT -\Documents\CM1-Dec 2024\New folder"

def is_csv_in_correct_format(file_path):
    """
    Checks if the CSV file is already in the correct format:
    - Ensures the delimiter is a semicolon.
    - Ensures all rows have the same number of columns.
    - Ensures the first column has a numeric value in European format (comma as decimal separator).
    """
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            rows = list(reader)

            # Check if the file is empty
            if not rows:
                print(f"File {file_path} is empty.")
                return False

            # Get the number of columns from the first row
            num_columns = len(rows[0])

            # Check for consistent column count
            for row in rows:
                if len(row) != num_columns:
                    print(f"Inconsistent column count in file {file_path}.")
                    return False  # Row has a different number of columns

                # Check if the first column is formatted correctly as a number
                if row[0]:
                    try:
                        # Try to convert first column to float using European formatting (comma as decimal separator)
                        float(row[0].replace(',', '.'))  # Replace comma with dot for float conversion
                    except ValueError:
                        print(f"First column in file {file_path} has an invalid format.")
                        return False  # If conversion fails, it's not a valid numeric format

            # If all checks pass, the file is in the correct format
            return True

    except Exception as e:
        print(f"Error checking format for {file_path}: {e}")
        return False


def update_csv_delimiter(folder_path, files_to_update=None):
    """
    Updates CSV files with correct semicolon delimiter and formats the first column.
    Skips files already in the correct format.
    """
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # List all files in the folder and print them for debugging
    print(f"Listing files in folder '{folder_path}':")
    files_in_folder = os.listdir(folder_path)
    print([os.path.join(folder_path, f) for f in files_in_folder])  # Debug: print full file paths

    # Check if any CSV files are present
    csv_files = [file for file in files_in_folder if file.lower().endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the folder.")
        return

    # Loop through the CSV files in the folder
    for filename in csv_files:
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {file_path}")

        # Skip files that are already in the correct format
        if is_csv_in_correct_format(file_path):
            print(f"Skipping file {filename} (already in correct format).")
            continue

        # Read the original CSV content
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                rows = list(csv.reader(file, delimiter=','))
                print(f"Read {len(rows)} rows from {file_path}")  # Check how many rows are read
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            continue

        updated_rows = []
        updated = False

        # Process each row
        for row in rows:
            print(f"Original row: {row}")  # Debugging row before modification
            updated_row = [column.replace(',', ';') for column in row]
            updated_row = [column.replace(' ', '') for column in updated_row]

            # Check and update the first column if it is not in European format
            if updated_row[0]:
                try:
                    # Convert the first column to a float, then format it with two decimal places
                    number = float(updated_row[0].replace(',', '.'))  # Convert European comma to dot for Python processing
                    updated_row[0] = f"{number:.2f}".replace('.', ',')  # Format to two decimals and convert dot to comma
                    updated = True
                except ValueError:
                    # If the value is not a number, keep it as-is
                    pass

            print(f"Updated row: {updated_row}")  # Debugging row after modification
            updated_rows.append(updated_row)

        # Write the updated content to the same file with semicolons as delimiters
        if updated:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerows(updated_rows)
                    print(f"Updated file written: {file_path}")
            except Exception as e:
                print(f"Error writing file {file_path}: {e}")
        else:
            print(f"No changes needed for {file_path}")

