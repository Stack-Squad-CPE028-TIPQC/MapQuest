import urllib.parse
import requests
import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
import webbrowser
from colorama import Fore, Style
from tabulate import tabulate

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "gTSwxlp8Zx8CHw1hcQpfLSCJVs7naX3E"

def get_directions():
    orig = entry_start.get()
    dest = entry_dest.get()
    unit = unit_var.get().lower()

    if not orig or not dest:
        messagebox.showerror("Error", "Please enter both Starting Location and Destination.")
        return

    if unit not in ["miles", "kilometers", "mi", "km"]:
        messagebox.showwarning("Warning", "Invalid unit. Defaulting to miles.")
        unit = "miles"

    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    json_data = requests.get(url).json()

    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        directions_text.delete(1.0, tk.END)
        directions_text.insert(tk.END, f"Directions from {orig} to {dest}\n")
        directions_text.insert(tk.END, f"Trip Duration: {json_data['route']['formattedTime']}\n")
        distance = json_data['route']['distance']
        if unit in ["kilometers", "km"]:
            distance = distance * 1.61
            unit_str = "Kilometers"
        else:
            unit_str = "Miles"
        directions_text.insert(tk.END, f"Distance: {distance:.2f} {unit_str}\n")
        directions_text.insert(tk.END, "=============================================\n")

        maneuvers = []
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            narrative = each["narrative"]
            dist = each["distance"] * (1.61 if unit in ["kilometers", "km"] else 1)
            maneuvers.append([narrative, f"{dist:.2f} {unit_str}"])
        
        directions_text.insert(tk.END, tabulate(maneuvers, headers=["Instruction", "Distance"], tablefmt="grid"))

        # Add link to open in MapQuest
        map_link = f"https://www.mapquest.com/directions/from/{orig.replace(' ', '+')}/to/{dest.replace(' ', '+')}"
        directions_text.insert(tk.END, f"\nOpen this route in MapQuest: {map_link}\n")
        open_map_button.config(state=tk.NORMAL)
        open_map_button.map_link = map_link
    elif json_status == 402:
        messagebox.showerror("Error", "Invalid user inputs for one or both locations.")
    elif json_status == 611:
        messagebox.showerror("Error", "Missing an entry for one or both locations.")
    else:
        messagebox.showwarning("Warning", f"For Status Code: {json_status}; Refer to: https://developer.mapquest.com/documentation/directions-api/status-codes")

def open_map():
    webbrowser.open(open_map_button.map_link)

# Create the main window
root = tk.Tk()
root.title("STACK SQUAD - MapQuest Directions App")
root.geometry("800x1000")
root.configure(bg="#F8F8F8")  # Light grey background for a modern look

# Load and resize the logo
try:
    logo = PhotoImage(file="C:/Users/Ken/Downloads/Visual Studio Code/devops/Project Activity 3 Social Coding/StackSmallest.png")

    # Resize the logo using subsample (scale down)
    max_width = 150
    max_height = 150
    width_ratio = logo.width() / max_width
    height_ratio = logo.height() / max_height
    scaling_factor = max(width_ratio, height_ratio)

    if scaling_factor > 1:
        logo = logo.subsample(int(scaling_factor))

    logo_label = tk.Label(root, image=logo, bg="#F8F8F8")
    logo_label.grid(row=0, column=0, columnspan=2, pady=10)
except tk.TclError:
    logo_label = tk.Label(root, text="STACK SQUAD", font=("Arial", 24, "bold"), bg="#F8F8F8", fg="#4B0082")
    logo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Style configuration
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#F8F8F8", foreground="#4B0082", font=("Arial", 14))  # Light background, purple text
style.configure("TButton", background="#FF6F00", foreground="white", font=("Arial", 14), padding=10)  # Orange button with white text, larger font
style.configure("TCombobox", font=("Arial", 12))

# Labels and entries for Starting Location and Destination
label_start = ttk.Label(root, text="Starting Location:")
label_start.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entry_start = ttk.Entry(root, width=40)
entry_start.grid(row=1, column=1, padx=10, pady=10)

label_dest = ttk.Label(root, text="Destination:")
label_dest.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
entry_dest = ttk.Entry(root, width=40)
entry_dest.grid(row=2, column=1, padx=10, pady=10)

# Dropdown for unit selection
label_unit = ttk.Label(root, text="Preferred Unit:")
label_unit.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
unit_var = tk.StringVar(value="miles")
unit_dropdown = ttk.Combobox(root, textvariable=unit_var, values=["miles", "kilometers"], state="readonly")
unit_dropdown.grid(row=3, column=1, padx=10, pady=10)

# Button to get directions
button_get_directions = ttk.Button(root, text="Get Directions", command=get_directions)
button_get_directions.grid(row=4, column=0, columnspan=2, pady=20)
button_get_directions.configure(style="TButton")

# Scrollable frame for directions
scrollable_frame = tk.Frame(root, bg="#F8F8F8", bd=2, relief="groove")
scrollable_frame.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

scrollbar = tk.Scrollbar(scrollable_frame, orient=tk.VERTICAL)
directions_text = tk.Text(scrollable_frame, wrap=tk.WORD, width=80, height=15, font=("Arial", 12), bg="#FFFFFF", fg="#4B0082", yscrollcommand=scrollbar.set, relief="flat")  # White background with purple text
scrollbar.config(command=directions_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
directions_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Button to open map link
open_map_button = ttk.Button(root, text="Open Map in Browser", command=open_map, state=tk.DISABLED)
open_map_button.grid(row=7, column=0, columnspan=2, pady=20)
open_map_button.configure(style="TButton")

# Start the main loop
root.mainloop()
