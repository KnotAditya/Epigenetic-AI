import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import importlib
import os

# Global variables
image_path = None

# Dynamically list cancer types
def get_cancer_types():
    folder = os.path.join(os.path.dirname(__file__), "Types_Experiment")
    files = [f[:-3] for f in os.listdir(folder) if f.endswith('.py') and not f.startswith('__')]
    return sorted(files)

# Upload image
def upload_image():
    global image_path
    image_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
    )
    if image_path:
        image_label.config(text=f"Uploaded: {os.path.basename(image_path)}")
    else:
        image_label.config(text="No image uploaded")

# Run prediction
def run_detection():
    cancer_type = cancer_type_var.get()
    if not cancer_type:
        messagebox.showerror("Error", "Please select a cancer type.")
        return

    if not image_path:
        messagebox.showerror("Error", "Please upload an image.")
        return

    try:
        module = importlib.import_module(f"Types_Experiment.{cancer_type}")
        if hasattr(module, 'predict'):
            result = module.predict(image_path)
            messagebox.showinfo("Detection Result", f"Prediction: {result}")
        else:
            messagebox.showerror("Error", f"The module '{cancer_type}' does not have a 'predict' function.")
    except Exception as e:
        messagebox.showerror("Execution Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Epigenetic AI - Early Cancer Detection")
root.geometry("1100x800")

# Upload section
tk.Button(root, text="Upload Image", command=upload_image).pack(pady=10)
image_label = tk.Label(root, text="No image uploaded")
image_label.pack()

# Cancer type selection
cancer_type_var = tk.StringVar()
tk.Label(root, text="Select Cancer Type:").pack(pady=(15, 0))
cancer_dropdown = ttk.Combobox(root, textvariable=cancer_type_var, values=get_cancer_types(), state='readonly')
cancer_dropdown.pack()

# Run
tk.Button(root, text="Run Detection", command=run_detection).pack(pady=20)

# Start GUI loop
root.mainloop()
