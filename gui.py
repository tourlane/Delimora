import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from datetime import datetime
import pandas as pd
from main import update_csv_delimiter, is_csv_in_correct_format


def list_csv_files(folder_path):
    """
    Lists all CSV files in the selected folder.
    """
    try:
        files_in_folder = os.listdir(folder_path)
        csv_files = [file for file in files_in_folder if file.lower().endswith('.csv')]
        return csv_files
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the folder: {e}")
        return []


def process_csv_files(folder_path, window):
    """
    Processes CSV files using update_csv_delimiter only if needed.
    """
    try:
        # List all CSV files in the folder
        csv_files = list_csv_files(folder_path)

        # Filter files that are not in the correct format
        files_to_update = [file for file in csv_files if not is_csv_in_correct_format(os.path.join(folder_path, file))]

        if files_to_update:
            # If there are files to update, process them
            update_csv_delimiter(folder_path, files_to_update)
            window.after(0, messagebox.showinfo, "Success", f"CSV files in folder '{folder_path}' have been updated!")
        else:
            window.after(0, messagebox.showinfo, "No Updates", "All CSV files are already in the correct format.")

        # Update the log with the list of processed files
        window.after(0, update_log, csv_files)

    except Exception as e:
        window.after(0, messagebox.showerror, "Error", f"An error occurred: {e}")


def update_log(files):
    """
    Updates the log text area with the list of processed CSV files.
    """
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, "Updated CSV Files:\n")
    for file in files:
        log_text.insert(tk.END, f"{file}\n")


def load_file(window):
    """
    Opens a folder selection dialog and starts processing CSV files.
    """
    folder_path = filedialog.askdirectory(title="Select Folder for CSV Files")
    if not folder_path:
        messagebox.showwarning("Warning", "No folder selected!")
        return

    # Run the processing in a separate thread to keep the GUI responsive
    threading.Thread(target=process_csv_files, args=(folder_path, window)).start()


def save_log():
    """
    Saves the log of processed files to an Excel or CSV file.
    """
    log_content = log_text.get(1.0, tk.END).strip().split("\n")

    if len(log_content) <= 1:
        messagebox.showwarning("Warning", "Log is empty or invalid!")
        return

    log_data = log_content[1:]  # Skip the header line

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"delimora_log_{timestamp}"

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        initialfile=default_filename,
        filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
    )

    if file_path:
        try:
            if file_path.endswith(".xlsx"):
                df = pd.DataFrame(log_data, columns=["File Names"])
                df.to_excel(file_path, index=False)
            elif file_path.endswith(".csv"):
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("File Names\n")
                    file.writelines(f"{line}\n" for line in log_data)

            messagebox.showinfo("Success", f"Log has been saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")


def create_gui():
    """
    Creates the main GUI application.
    """
    global log_text
    window = tk.Tk()
    window.title("Gringotts - Delimora")
    window.geometry("900x500")
    window.configure(bg="#2C2F36")

    # Header Section with Sparkles
    header_frame = tk.Frame(window, bg="#2C2F36")
    header_frame.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="ew")
    header_frame.columnconfigure(0, weight=1)

    title_label = tk.Label(
        header_frame,
        text="✨ Delimora ✨",
        font=("Helvetica", 24, "bold"),
        fg="#FFD700",
        bg="#2C2F36",
    )
    title_label.grid(row=0, column=0, sticky="nsew")

    subtitle_label = tk.Label(
        header_frame,
        text="A Magical Way to Manage CSV Files",
        font=("Helvetica", 12, "italic"),
        fg="white",
        bg="#2C2F36",
    )
    subtitle_label.grid(row=1, column=0, sticky="nsew", pady=(5, 0))

    # Log Section
    log_text = tk.Text(window, height=15, wrap="word", bg="#353C47", fg="white", font=("Courier", 12))
    log_text.grid(row=1, column=0, pady=(5, 10), padx=10, sticky="nsew")

    # Buttons Section
    button_frame = tk.Frame(window, bg="#2C2F36")
    button_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    select_button = tk.Button(
        button_frame,
        text="🔄 Load Folder for CSVs",
        command=lambda: load_file(window),
        bg="#4A90E2",
        fg="white",
        font=("Helvetica", 12, "bold"),
        relief="flat",
        padx=20,
        pady=10,
    )
    select_button.grid(row=0, column=0, pady=5, sticky="ew")

    save_button = tk.Button(
        button_frame,
        text="💾 Download Log",
        command=save_log,
        bg="#4A90E2",
        fg="white",
        font=("Helvetica", 12, "bold"),
        relief="flat",
        padx=20,
        pady=10,
    )
    save_button.grid(row=0, column=1, pady=5, sticky="ew")


    # Allow resizing of the log text area
    window.grid_rowconfigure(1, weight=1)  # Log text expands vertically
    window.grid_columnconfigure(0, weight=1)  # Log text expands horizontally

    window.mainloop()


# Create the GUI
create_gui()
