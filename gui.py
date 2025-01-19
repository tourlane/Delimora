import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from datetime import datetime
import pandas as pd
import openpyxl


def list_csv_files(folder_path):
    try:
        files_in_folder = os.listdir(folder_path)
        csv_files = [file for file in files_in_folder if file.lower().endswith('.csv')]
        return csv_files
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the folder: {e}")
        return []

def load_file(window):
    folder_path = filedialog.askdirectory()
    if not folder_path:
        messagebox.showwarning("Warning", "No folder selected!")
        return
    threading.Thread(target=process_csv_files, args=(folder_path, window)).start()

def process_csv_files(folder_path, window):
    try:
        csv_files = list_csv_files(folder_path)
        window.after(0, update_log, csv_files, window)
        window.after(0, messagebox.showinfo, "Success", f"CSV files in folder '{folder_path}' have been listed!")
    except Exception as e:
        window.after(0, messagebox.showerror, "Error", f"An error occurred: {e}")

def update_log(files, window):
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, "Updated CSV Files:\n")
    for file in files:
        log_text.insert(tk.END, f"{file}\n")


def save_log():
    log_content = log_text.get(1.0, tk.END).strip().split("\n")

    if len(log_content) <= 1:
        messagebox.showwarning("Warning", "Log is empty or invalid!")
        return

    if log_content[0].startswith("CSV Files in Folder:"):
        log_data = log_content[1:]
    else:
        log_data = log_content

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
                try:
                    import openpyxl  # Check if openpyxl is installed
                    df = pd.DataFrame(log_data, columns=["File Names"])
                    df.to_excel(file_path, index=False)
                except ImportError:
                    messagebox.showerror(
                        "Missing Library",
                        "The 'openpyxl' library is required to save as Excel. Please install it using:\n\npip install openpyxl"
                    )
                    return
            elif file_path.endswith(".csv"):
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("File Names\n")
                    file.writelines(f"{line}\n" for line in log_data)

            messagebox.showinfo("Success", f"Log has been saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

def create_gui():
    global log_text
    window = tk.Tk()
    window.title("Gringotts - Delimora")
    window.geometry("600x500")
    window.configure(bg="#2C2F36")

    # Header Section with Sparkles
    header_frame = tk.Frame(window, bg="#2C2F36")
    header_frame.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="ew")
    header_frame.columnconfigure(0, weight=1)

    # Sparkling Title
    title_text = "✨ Delimora ✨"
    title_label = tk.Label(
        header_frame,
        text=title_text,
        font=("Helvetica", 24, "bold"),
        fg="#FFD700",  # Gold color for the text
        bg="#2C2F36",
    )
    title_label.grid(row=0, column=0, sticky="nsew")

    # Subtitle
    subtitle_label = tk.Label(
        header_frame,
        text="A Magical Way to Manage CSV Files",
        font=("Helvetica", 12, "italic"),
        fg="white",
        bg="#2C2F36",
    )
    subtitle_label.grid(row=1, column=0, sticky="nsew", pady=(5, 0))

    # Log Section
    log_text = tk.Text(window, height=15, wrap="word", font=("Courier New", 12), bg="#1A1D23", fg="white", bd=0)
    log_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Buttons Section
    button_frame = tk.Frame(window, bg="#2C2F36")
    button_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    # Load Folder Button
    load_button = tk.Button(
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
    load_button.grid(row=0, column=0, padx=5, sticky="ew")

    # Download Log Button
    download_button = tk.Button(
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
    download_button.grid(row=0, column=1, padx=5, sticky="ew")

    # Allow resizing of the log text area
    window.grid_rowconfigure(1, weight=1)  # Log text expands vertically
    window.grid_columnconfigure(0, weight=1)  # Log text expands horizontally

    # Start the GUI loop
    window.mainloop()

# Run the GUI
create_gui()
