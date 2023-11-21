import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess

def run_advanced_configuration():
    try:
        subprocess.Popen(["python", "1.py"])
    except FileNotFoundError:
        add_text("Archivo '1.py' no encontrado.", "debug")
    except Exception as e:
        add_text(f"Error al ejecutar '1.py': {str(e)}", "debug")

def get_config_path():
    try:
        with open('config.conf', 'r') as config_file:
            lines = config_file.readlines()
            for line in lines:
                if 'config.json Path:' in line:
                    path = line.split(': ')[1].strip()
                    return path
        return None
    except FileNotFoundError:
        return None

def get_raw_dataset_path():
    try:
        with open('config.conf', 'r') as config_file:
            lines = config_file.readlines()
            for line in lines:
                if 'Raw Dataset Path:' in line:
                    raw_path = line.split(': ')[1].strip()
                    return raw_path
        return None
    except FileNotFoundError:
        return None

def execute_command(command):
    if command == "svc train -t":
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            add_text(line.strip(), "debug")
        process.wait()
        if process.returncode == 0:
            add_text("Command executed successfully.", "result", "green")
        else:
            add_text("Error executing the command.", "result", "red")
    else:
        raw_path = get_raw_dataset_path()
        if raw_path:
            command = f"{command} -i {raw_path}"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                add_text(line.strip(), "debug")
            process.wait()
            if process.returncode == 0:
                add_text("Command executed successfully.", "result", "green")
            else:
                add_text("Error executing the command.", "result", "red")
        else:
            add_text("Failed to obtain the raw dataset path.", "debug")

def add_text(text, type, color=None):
    if type == "result":
        text_box.tag_configure(type, foreground=color)
        text_box.insert(tk.END, text + "\n", type)
    else:
        text_box.insert(tk.END, text + "\n")
    text_box.see(tk.END)

def action_button_one():
    execute_command("svc pre-resample")

def action_button_two():
    execute_command("svc pre-config")

def action_button_three():
    execute_command("svc pre-hubert")

def action_button_four():
    execute_command("svc train -t")

def action_button_config():
    def select_config_path():
        window.grab_release()
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        config_path_entry.delete(0, tk.END)
        config_path_entry.insert(0, path)
        window.grab_set()

    def select_raw_dataset_path():
        window.grab_release()
        path = filedialog.askdirectory()
        raw_path_entry.delete(0, tk.END)
        raw_path_entry.insert(0, path)
        window.grab_set()

    config_window = tk.Toplevel(window)
    config_window.title("Configuration")

    config_window_width = 400
    config_window_height = 250
    x_pos = (window.winfo_screenwidth() // 2) - (config_window_width // 2)
    y_pos = (window.winfo_screenheight() // 2) - (config_window_height // 2)
    config_window.geometry(f"{config_window_width}x{config_window_height}+{x_pos}+{y_pos}")

    label_config_json = tk.Label(config_window, text="Enter the path for the config.json file:")
    label_config_json.pack()

    config_path_current = get_config_path()
    config_path_entry = tk.Entry(config_window, width=50)
    config_path_entry.insert(0, config_path_current if config_path_current else "")
    config_path_entry.pack()



    label_raw_path = tk.Label(config_window, text="Enter the Raw Dataset Path:")
    label_raw_path.pack()

    raw_path_current = get_raw_dataset_path()
    raw_path_entry = tk.Entry(config_window, width=50)
    raw_path_entry.insert(0, raw_path_current if raw_path_current else "")
    raw_path_entry.pack()


    def save_config():
        config_path = config_path_entry.get()
        raw_path = raw_path_entry.get()
        with open('config.conf', 'w') as config_file:
            config_file.write(f"config.json Path: {config_path}\n")
            config_file.write(f"Raw Dataset Path: {raw_path}")
        config_window.destroy()

    button_save = tk.Button(config_window, text="Save", command=save_config)
    button_save.pack()

    button_cancel = tk.Button(config_window, text="Cancel", command=config_window.destroy)
    button_cancel.pack()

def show_help():
    help_window = tk.Toplevel(window)
    help_window.title("Help")
    
    help_window_width = 400
    help_window_height = 300
    
    x_pos_help = (window.winfo_screenwidth() // 2) - (help_window_width // 2)
    y_pos_help = (window.winfo_screenheight() // 2) - (help_window_height // 2)
    
    help_window.geometry(f"{help_window_width}x{help_window_height}+{x_pos_help}+{y_pos_help}")

    text = tk.Text(help_window)
    text.pack()

    with open('help.txt', 'r') as help_file:
        content = help_file.read()
        text.insert(tk.END, content)
    text.config(state=tk.DISABLED)

window = tk.Tk()
window.title("Sovits Train Interface")

window_width = 450
window_height = 400

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

button_container = tk.Frame(window)
button_container.pack(pady=10)

text_box = tk.Text(window, height=15, width=40)
text_box.pack(padx=10)
text_box.config(width=80)

image_pre_sample = Image.open("images/presample.png").resize((35, 35))
image_pre_sample = ImageTk.PhotoImage(image_pre_sample)

image_pre_config = Image.open("images/preconfig.png").resize((35, 35))
image_pre_config = ImageTk.PhotoImage(image_pre_config)

image_pre_hubert = Image.open("images/prehubert.png").resize((35, 35))
image_pre_hubert = ImageTk.PhotoImage(image_pre_hubert)

image_train = Image.open("images/train.png").resize((35, 35))
image_train = ImageTk.PhotoImage(image_train)

image_config = Image.open("images/config.png").resize((35, 35))
image_config = ImageTk.PhotoImage(image_config)

button_one = tk.Button(button_container, image=image_pre_sample, command=action_button_one)
button_one.pack(side=tk.LEFT, padx=10)

button_two = tk.Button(button_container, image=image_pre_config, command=action_button_two)
button_two.pack(side=tk.LEFT, padx=10)

button_three = tk.Button(button_container, image=image_pre_hubert, command=action_button_three)
button_three.pack(side=tk.LEFT, padx=10)

button_four = tk.Button(button_container, image=image_train, command=action_button_four)
button_four.pack(side=tk.LEFT, padx=10)

button_config = tk.Button(button_container, image=image_config, command=action_button_config)
button_config.pack(side=tk.LEFT, padx=10)

image_help = Image.open("images/help.png").resize((35, 35))
image_help = ImageTk.PhotoImage(image_help)

button_help = tk.Button(button_container, image=image_help, command=show_help)
button_help.pack(side=tk.RIGHT, padx=10)
# Nuevo botón "Sovits Advanced Configuration"
image_advanced_config = Image.open("images/advanced_config.png").resize((35, 35))
image_advanced_config = ImageTk.PhotoImage(image_advanced_config)

def action_advanced_config():
    run_advanced_configuration()

button_advanced_config = tk.Button(button_container, image=image_advanced_config, command=action_advanced_config)
button_advanced_config.pack(side=tk.LEFT, padx=10)

window.mainloop()

