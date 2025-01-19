import os
import csv

folder_path = r"C:\Users\LT -\Documents\Test\New folder"

def update_csv_delimiter(folder_path):
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

        # Read the original CSV content
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                rows = list(csv.reader(file))
                print(f"Read {len(rows)} rows from {file_path}")  # Check how many rows are read
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            continue

        updated_rows = []

        # Process each row
        for row in rows:
            print(f"Original row: {row}")  # Debugging row before modification
            # Replace commas with semicolons in all columns (except the first one)
            updated_row = [column.replace(',', ';') for column in row]
            updated_row = [column.replace(' ', '') for column in row]

            # Check and update the first column if it is not in European format
            if updated_row[0]:
                try:
                    # Convert the first column to a float, then format it with two decimal places
                    number = float(
                        updated_row[0].replace(',', '.'))  # Convert European comma to dot for Python processing
                    updated_row[0] = f"{number:.2f}".replace('.',
                                                             ',')  # Format to two decimals and convert dot to comma
                except ValueError:
                    # If the value is not a number, keep it as-is
                    pass

            print(f"Updated row: {updated_row}")  # Debugging row after modification
            # Append the updated row to the list
            updated_rows.append(updated_row)

        # Write the updated content to the same file with semicolons as delimiters
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(updated_rows)
                print(f"Updated file written: {file_path}")
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")

# Run the update function on the target folder
update_csv_delimiter(folder_path)
