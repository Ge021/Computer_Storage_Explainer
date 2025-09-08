import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading


def get_folder_size(folder_path):
    total = 0

    for dirpath, _, filenames in os.walk(folder_path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total += os.path.getsize(fp)

            except (PermissionError, FileNotFoundError):
                pass
    return total

def format_size(size_bytes):
    if size_bytes >= 1024**3:
        return f"{size_bytes / (1024**3):.2f} GB"
    else:
        return f"{size_bytes / (1024**2):.2f} MB"


def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, folder)

def scan_folder_thread():
    threading.Thread(target=scan_folder).start()

def scan_folder():
    folder = entry_path.get()
    if not os.path.isdir(folder):
        messagebox.showerror("Error", "Invalid folder path")
        return

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Scanning folder...\n")

    sizes = {}
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isdir(item_path):
            size = get_folder_size(item_path)
            sizes[item] = size

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"{'Folder':<40}: {'Size':>10}\n")
    output_text.insert(tk.END, "-"*52 + "\n")

    for folder_name, size_bytes in sorted(sizes.items(), key=lambda x: x[1], reverse=True):
        output_text.insert(tk.END, f"{folder_name:<40}: {format_size(size_bytes):>10}\n")


root = tk.Tk()
root.title("Computer Storage Explainer")
root.geometry("600x500")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

entry_path = tk.Entry(frame_top, width=40)
entry_path.grid(row=0, column=0, padx=5)

btn_browse = tk.Button(frame_top, text="Browse", command=browse_folder)
btn_browse.grid(row=0, column=1, padx=5)

btn_scan = tk.Button(frame_top, text="Scan Folder", command=scan_folder_thread)
btn_scan.grid(row=0, column=2, padx=5)


output_text = scrolledtext.ScrolledText(root, height=25, width=70)
output_text.pack(padx=10, pady=10)

root.mainloop()
