import os
import csv

def update_csv_delimiter(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return []

    files_in_folder = os.listdir(folder_path)
    csv_files = [file for file in files_in_folder if file.lower().endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the folder.")
        return []

    updated_files = []  # List to store names of updated files

    for filename in csv_files:
        file_path = os.path.join(folder_path, filename)

        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                rows = list(csv.reader(file))
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            continue  # Skip this file and move on to the next

        updated_rows = []

        for row in rows:
            updated_row = [column.replace(',', ';') for column in row]
            updated_row = [column.replace(' ', '') for column in row]

            if updated_row[0]:
                try:
                    number = float(updated_row[0].replace(',', '.'))
                    updated_row[0] = f"{number:.2f}".replace('.', ',')
                except ValueError:
                    pass

            updated_rows.append(updated_row)

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(updated_rows)
            updated_files.append(filename)  # Add updated file to the list
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
            continue  # Skip this file and move on to the next

    return updated_files  # Return the list of updated files