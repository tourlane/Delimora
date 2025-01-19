import os
import csv

folder_path = r"C:\Users\LT -\Documents\CM1-Nov 2024\New folder"
summary_file_path = os.path.join(folder_path, "Totals_Summary.csv")

def update_csv_delimiter(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # Prepare to write the summary file
    totals_summary = []

    # List all files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the folder.")
        return

    # Loop through the CSV files in the folder
    for filename in csv_files:
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {file_path}")

        total_amount = 0.0
        total_balance = 0.0  # For the balance column

        # Read the original CSV content without modifying it
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                rows = list(csv.reader(file))
                print(f"Read {len(rows)} rows from {file_path}")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            continue

        # Process each row and sum the first column
        for row in rows:
            if not row:  # Skip empty rows
                continue

            try:
                # Convert to float and calculate the total for the first column
                number = float(row[0].replace(',', '.'))
                total_amount += number

                # Check the second column and adjust balance accordingly
                if row[1] == 'H':  # For "H", subtract from balance
                    total_balance -= number
                    print(f"Subtracting {number} for 'H', New Balance: {total_balance}")
                else:  # For any other value (assumed "S"), add to balance
                    total_balance += number
                    print(f"Adding {number} for 'S', New Balance: {total_balance}")
            except ValueError:
                pass  # Ignore rows where the first column isn't a number

        # Add the total for the current file to the summary
        totals_summary.append([filename, f"{total_amount:.2f}".replace('.', ','), f"{total_balance:.2f}".replace('.', ',')])

    # Write the totals summary to a new file
    try:
        with open(summary_file_path, mode='w', newline='', encoding='utf-8') as summary_file:
            writer = csv.writer(summary_file, delimiter=';')
            writer.writerow(["Filename", "Total Amount", "Balance"])
            writer.writerows(totals_summary)
            print(f"Summary file written: {summary_file_path}")
    except Exception as e:
        print(f"Error writing summary file {summary_file_path}: {e}")

# Run the update function on the target folder
update_csv_delimiter(folder_path)
