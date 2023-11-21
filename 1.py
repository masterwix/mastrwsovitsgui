import tkinter as tk
from tkinter import ttk
import json
import os
import shutil
from datetime import datetime
from tkinter import messagebox

CONFIG_PATH = os.path.join('configs', '44k', 'config.json')
BACKUP_FOLDER = 'config-backups'

# Variable para controlar si los datos han sido salvados
data_saved = False

def get_config_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.conf')
    
    paths = {}
    if os.path.exists(config_path):
        with open(config_path, 'r') as conf_file:
            lines = conf_file.readlines()
            for line in lines:
                parts = line.strip().split(': ')
                if len(parts) == 2:
                    key, value = parts[0], parts[1]
                    paths[key] = value
                else:
                    print(f"Ignoring line: {line}")
        return paths
    else:
        print("Configuration file 'config.conf' not found.")
        return None

def load_config():
    paths = get_config_paths()
    if paths and 'config.json Path' in paths:
        json_path = paths['config.json Path']
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r') as file:
                    config_data = json.load(file)
                return config_data
            except FileNotFoundError:
                print(f"Configuration file '{json_path}' not found.")
                return None
        else:
            print(f"Config.json file '{json_path}' not found.")
            return None
    else:
        print("Invalid or missing 'config.json Path' in config.conf.")
        return None

def save_config(config):
    global data_saved  # Acceder a la variable global
    paths = get_config_paths()
    if paths and 'config.json Path' in paths:
        json_path = paths['config.json Path']
        if os.path.exists(json_path):
            # Crear la carpeta config-backups si no existe
            backup_folder = os.path.join(os.getcwd(), BACKUP_FOLDER)
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)
            
            try:
                # Crear el nombre del archivo de backup
                backup_file = f"config_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
                # Copiar el archivo de configuración a la carpeta de backups
                shutil.copyfile(json_path, os.path.join(backup_folder, backup_file))

                with open(json_path, 'w') as file:
                    json.dump(config, file, indent=4)
                print("Data saved to configuration file.")
                data_saved = True  # Marcar los datos como salvados
            except Exception as e:
                print(f"Error saving data: {e}")
        else:
            print(f"Config.json file '{json_path}' not found.")
    else:
        print("Invalid or missing 'config.json Path' in config.conf.")

def save_or_cancel(root, config, close_window=False):
    global data_saved  # Acceder a la variable global
    if close_window:
        if not data_saved:  # Verificar si los datos no se han salvado
            if not messagebox.askokcancel("Warning", "Changes will not be saved. Continue?"):
                return
    
    if close_window or messagebox.askokcancel("Save Changes", "Save and close?"):
        save_config(config)
        root.destroy()

def show_config_tab(tab, section_data):
    def update_config(key, value):
        section_data[key] = value
        backup_config()

    row = 0
    column = 0
    for category, value in section_data.items():
        label = ttk.Label(tab, text=f"{category}:")
        label.grid(column=column, row=row, padx=5, pady=5, sticky='w')

        entry_var = tk.StringVar(value=str(value))
        entry = ttk.Entry(tab, width=25, textvariable=entry_var)
        entry.grid(column=column + 1, row=row, padx=5, pady=5, sticky='w')

        entry_var.trace_add('write', lambda name, index, mode, var=entry_var, key=category: update_config(key, var.get()))

        row += 1
        if row % 10 == 0:
            row = 0
            column += 2

def main():
    root = tk.Tk()
    root.title("Training Configuration")
    root.configure(bg="white")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    config = load_config()

    if config:
        tab_control = ttk.Notebook(root)

        for section, section_data in config.items():
            section_name = "Data" if section == "data" else "Raw Data Location" if section == "files" else section
            section_tab = ttk.Frame(tab_control)
            tab_control.add(section_tab, text=section_name)

            show_config_tab(section_tab, section_data)

        tab_control.pack(expand=1, fill='both')

        buttons_frame = ttk.Frame(root)
        buttons_frame.pack()

        save_button = ttk.Button(buttons_frame, text="Save", command=lambda: save_or_cancel(root, config))
        save_button.grid(row=0, column=0, padx=5, pady=10)

        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=lambda: save_or_cancel(root, config, close_window=True))
        cancel_button.grid(row=0, column=1, padx=5, pady=10)

        root.protocol("WM_DELETE_WINDOW", lambda: save_or_cancel(root, config, close_window=True))

        root.update_idletasks()
        window_width = root.winfo_width()
        window_height = root.winfo_height()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        root.mainloop()

if __name__ == "__main__":
    main()

