import os
import csv

def convert_column_0_format(file_path):
    # Read the original CSV content
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            rows = list(csv.reader(file, delimiter=';'))  # Read the CSV with ; as delimiter
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return

    updated_rows = []

    # Process each row
    for row in rows:
        if row[0]:  # Check if there's a value in the first column
            # Replace semicolon with comma in the first column if necessary
            if ';' in row[0]:
                row[0] = row[0].replace(';', ',')  # Change semicolon to comma
        updated_rows.append(row)

    # Write the updated content back to the same file with semicolons as delimiters
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(updated_rows)
            print(f"Updated file written: {file_path}")
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")

def update_csv_in_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # List all files in the folder
    files_in_folder = os.listdir(folder_path)

    # Check if any CSV files are present
    csv_files = [file for file in files_in_folder if file.lower().endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the folder.")
        return

    # Loop through the CSV files in the folder
    for filename in csv_files:
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {file_path}")

        # Call the function to convert the first column format
        convert_column_0_format(file_path)

# Example usage
folder_path = r"C:\Users\LT -\Documents\CM1-Oct 2024\New folder"
update_csv_in_folder(folder_path)
