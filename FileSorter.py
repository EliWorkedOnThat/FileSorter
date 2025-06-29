import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# File categories
file_types = {
    "Images": ['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv'],
    'Music': ['.mp3', '.wav', '.aac'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.sh', '.bat'],
}

def create_gui():
    root = tk.Tk()
    root.title("File Sorter")
    root.geometry("600x550")
    root.resizable(False, False)

    # PATH Label
    path_label = tk.Label(root, text="Folder Path:")
    path_label.pack(pady=(10, 0))

    # Entry Field
    path_var = tk.StringVar()
    path_entry = tk.Entry(root, textvariable=path_var, width=60)
    path_entry.pack(padx=10, pady=5)

    # Browse Button
    def browse_folder():
        selected = filedialog.askdirectory()
        if selected:
            path_var.set(selected)

    browse_button = tk.Button(root, text="Browse", command=browse_folder)
    browse_button.pack(pady=5)

    # Sort Order Option (added size options)
    sort_order_var = tk.StringVar(value="A to Z")
    sort_order_label = tk.Label(root, text="Sort Order:")
    sort_order_label.pack(pady=(10, 0))

    sort_order_menu = tk.OptionMenu(root, sort_order_var, "A to Z", "Z to A", "Smallest to Biggest", "Biggest to Smallest")
    sort_order_menu.pack(pady=5)

    # Output Log (scrollable)
    log_output = scrolledtext.ScrolledText(root, width=70, height=18)
    log_output.pack(padx=10, pady=10)

    # Sorting Function
    def sort_files():
        path = path_var.get().strip()
        path = path.replace('"', '').replace("'", '')
        log_output.delete("1.0", tk.END)  # Clear previous logs

        if not os.path.isdir(path):
            messagebox.showerror("Invalid Path", "The specified path is not a valid folder.")
            return

        log_output.insert(tk.END, f"✅ Folder found: {path}\nSorting files and folders...\n\n")

        items = os.listdir(path)
        sort_option = sort_order_var.get()

        if sort_option == "A to Z":
            items.sort()
        elif sort_option == "Z to A":
            items.sort(reverse=True)
        elif sort_option == "Smallest to Biggest":
            # Separate files and folders
            files = [f for f in items if os.path.isfile(os.path.join(path, f))]
            folders = [f for f in items if os.path.isdir(os.path.join(path, f))]
            # Sort files by ascending size
            files.sort(key=lambda f: os.path.getsize(os.path.join(path, f)))
            folders.sort()  # folders alphabetically after files
            items = files + folders
        elif sort_option == "Biggest to Smallest":
            files = [f for f in items if os.path.isfile(os.path.join(path, f))]
            folders = [f for f in items if os.path.isdir(os.path.join(path, f))]
            # Sort files by descending size
            files.sort(key=lambda f: os.path.getsize(os.path.join(path, f)), reverse=True)
            folders.sort()
            items = files + folders

        for item in items:
            item_path = os.path.join(path, item)

            if os.path.isfile(item_path):
                _, ext = os.path.splitext(item)
                ext = ext.lower()
                moved = False

                for category, extensions in file_types.items():
                    if ext in extensions:
                        dest_folder = os.path.join(path, category)
                        os.makedirs(dest_folder, exist_ok=True)
                        os.rename(item_path, os.path.join(dest_folder, item))
                        log_output.insert(tk.END, f"Moved file '{item}' to '{category}'\n")
                        moved = True
                        break

                if not moved:
                    dest_folder = os.path.join(path, "Others")
                    os.makedirs(dest_folder, exist_ok=True)
                    os.rename(item_path, os.path.join(dest_folder, item))
                    log_output.insert(tk.END, f"Moved file '{item}' to 'Others'\n")

            elif os.path.isdir(item_path):
                dest_folder = os.path.join(path, "Others")
                os.makedirs(dest_folder, exist_ok=True)
                try:
                    shutil.move(item_path, os.path.join(dest_folder, item))
                    log_output.insert(tk.END, f"Moved folder '{item}' to 'Others'\n")
                except Exception as e:
                    log_output.insert(tk.END, f"Error moving folder '{item}': {e}\n")
            else:
                log_output.insert(tk.END, f"Skipping unknown item: {item}\n")

            log_output.see(tk.END)

        log_output.insert(tk.END, "\n✅ Sorting completed!\n")
        log_output.see(tk.END)

    # Sort Button
    sort_button = tk.Button(root, text="Sort Files", command=sort_files, bg="#4CAF50", fg="white", height=2, width=15)
    sort_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
