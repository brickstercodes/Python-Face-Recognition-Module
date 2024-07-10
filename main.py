import cv2
import os
import tkinter as tk
from tkinter import simpledialog
import subprocess
from tkinter import PhotoImage

# Folder where face data is stored
datasets = 'D:\\Python FaceRecogModule\\recog\\datasets'

# Global variable to track whether capturing/recognizing is ongoing
capturing = False
recognizing = False

def add_faces():
    # Disable buttons and update status label
    add_faces_button.config(state=tk.DISABLED)
    recognize_face_button.config(state=tk.DISABLED)
    list_faces_button.config(state=tk.DISABLED)

    # Get the person's name from the user
    person_name = simpledialog.askstring("Input", "Enter the person's name:")
    if not person_name:
        # If name is empty, show an error message
        tk.messagebox.showerror("Error", "Please provide a valid name.")
        capturing = False
        return

    # Check if the name already exists in the datasets directory
    person_path = os.path.join(datasets, person_name)
    if os.path.exists(person_path):
        # If name already exists, show an error message
        tk.messagebox.showerror("Error", "Name already exists. Please choose a different name.")
        capturing = False
        return

    # Run the create_data script with the provided person's name
    subprocess.run(["python", "D:\\Python FaceRecogModule\\recog\\add_face_data.py", person_name])

    # After capturing is done, re-enable buttons and clear status label
    add_faces_button.config(state=tk.NORMAL)
    recognize_face_button.config(state=tk.NORMAL)
    list_faces_button.config(state=tk.NORMAL)

# Function to handle recognizing faces
def recognize_face():
    # Disable buttons and update status label
    add_faces_button.config(state=tk.DISABLED)
    recognize_face_button.config(state=tk.DISABLED)
    list_faces_button.config(state=tk.DISABLED)
    status_label.config(text="Recognizing Faces..., Press ESC to close")
    root.update()  # Force UI update

    # Run the recognition script
    subprocess.run(["python", "D:\\Python FaceRecogModule\\recog\\face_recognize.py"])

    # After recognition is done, re-enable buttons and clear status label
    add_faces_button.config(state=tk.NORMAL)
    recognize_face_button.config(state=tk.NORMAL)
    list_faces_button.config(state=tk.NORMAL)
    status_label.config(text="")

# Function to list available faces
def list_available_faces():    
    available_faces = subprocess.run(["python", "D:\\Python FaceRecogModule\\recog\\list_faces.py"], capture_output=True, text=True)
    # Create a new window to display the available faces list
    result_window = tk.Toplevel(root)
    result_window.title("Available Face Data")

    # Display the available faces list with appropriate formatting
    result_label = tk.Label(result_window, text=available_faces.stdout, font=("Helvetica", 12))
    result_label.pack(padx=20, pady=20)

    # Add a close button to the result window
    close_button = tk.Button(result_window, text="Close", command=result_window.destroy, padx=20, pady=10)
    close_button.pack(pady=10)

# Create the main application window
root = tk.Tk()
root.title("Face Recognizer")
root.geometry("1920x1080")
logo_path = "D:\\Python FaceRecogModule\\recog\\Window_Logo.ico"  # Path to the logo imawge file (It has to be a .ico file)

# Set the logo for the window
root.iconbitmap(logo_path)

# Define colors
background_color = "#fbe7ac"
button_color = "#45958e"
button_text_color = "#fbe7ac"
title_text_color = "dark red"
status_text_color = "#fad4a6"

root.configure(bg=background_color)
title_label = tk.Label(root, text="Face Recognition for Polarizer", font=("OpenSans", 60, "bold"), fg=title_text_color, bg=background_color)
title_label.pack(pady=40)

# Create a frame to contain the buttons
button_frame = tk.Frame(root, bg=background_color, bd=5, relief=tk.SUNKEN)
button_frame.pack(pady=20)

# Load image icons
# Load image icons with resizing
add_icon = PhotoImage(file="C:\\Users\\sande\\Desktop\\ocv\\add.png").subsample(2, 2)  # Adjust subsampling factor as needed
recog_icon = PhotoImage(file="C:\\Users\\sande\\Desktop\\ocv\\recog.png").subsample(2, 2)
list_icon = PhotoImage(file="C:\\Users\\sande\\Desktop\\ocv\\list.png").subsample(2, 2)

# Create buttons with icons
add_faces_button = tk.Button(button_frame, text="Add Faces", command=add_faces, image=add_icon, compound=tk.TOP, padx=30, pady=15, bg=button_color, fg=button_text_color, font=("Helvetica", 25, "bold"), border=10)
add_faces_button.pack(side=tk.LEFT, padx=10)

recognize_face_button = tk.Button(button_frame, text="Recognize Face", command=recognize_face, image=recog_icon, compound=tk.TOP, padx=30, pady=15, bg=button_color, fg=button_text_color, font=("Helvetica", 25, "bold"), border=10)
recognize_face_button.pack(side=tk.LEFT, padx=10)

list_faces_button = tk.Button(button_frame, text="List Available Faces", command=list_available_faces, image=list_icon, compound=tk.TOP, padx=30, pady=15, bg=button_color, fg=button_text_color, font=("Helvetica", 25, "bold"), border=10)
list_faces_button.pack(side=tk.LEFT, padx=10)


status_label = tk.Label(root, text="", font=("Segoe UI", 16), fg=status_text_color, bg=background_color, border=10)
status_label.pack(pady=20)

# Start the main UI loop
root.mainloop()