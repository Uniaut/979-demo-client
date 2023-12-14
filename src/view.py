import cv2
import tkinter as tk
from PIL import ImageTk, Image

import numpy as np


class WebcamContentSection(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="gray")

        self.webcam_area = tk.Canvas(self, bg="gray")
        self.webcam_area.pack(padx=10, pady=10, fill="both", expand=True)

        self.action_button = tk.Button(self, text="Action")
        self.action_button.pack(side="bottom", padx=10, pady=10)
    

    def update(self, frame):
        # resize the frame to fit the canvas
        self.webcam_area.update()
        cv2.flip(frame, 1, frame)
        frame = cv2.resize(frame, (self.webcam_area.winfo_width(), self.webcam_area.winfo_height()))

        # Convert the frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(frame, mode="RGB")

        # create dummy image
        # image = Image.new("RGB", (300, 200), (255, 0, 0))
        
        image = ImageTk.PhotoImage(image=image)
        self.webcam_area.create_image(0, 0, image=image, anchor="nw")
        self.webcam_area.image_names = image

        

class DetectedItemsSection(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="white")

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True)
    
    def update(self):
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, f"Item {np.random.randint(0, 100)}")