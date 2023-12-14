import cv2
import tkinter as tk
from PIL import ImageTk, Image

import numpy as np


class WebcamContentSection(tk.Frame):
    def __init__(self, master, action: callable, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="gray")
        self.action = action

        self.webcam = cv2.VideoCapture(0)
        
        self.webcam_area = tk.Canvas(self, bg="gray")
        self.webcam_area.pack(padx=10, pady=10, fill="both", expand=True)

        self.action_button = tk.Button(self, text="Capture", command=self.action)
        self.action_button.pack(side="bottom", padx=10, pady=10)


    def update(self, frame):
        # resize the frame to fit the canvas
        self.webcam_area.update()
        frame = cv2.resize(frame, (self.webcam_area.winfo_width(), self.webcam_area.winfo_height()))

        image = Image.fromarray(frame, mode="RGB")

        # create dummy image
        # image = Image.new("RGB", (300, 200), (255, 0, 0))
        
        image = ImageTk.PhotoImage(image=image)
        self.webcam_area.create_image(0, 0, image=image, anchor="nw")
        self.webcam_area.image_names = image


    def update_preview(self):
        # get a frame from the webcam
        _, frame = self.webcam.read()   
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.flip(frame, 1, frame)    

        self.update(frame)

        return frame
    
    
    def update_predicted(self, image):
        self.update(image)


class DetectedItemsSection(tk.Frame):
    def __init__(self, master, action, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="white")
        self.action = action

        self.listbox = tk.Listbox(self, font=("Arial", 15))
        self.listbox.pack(fill="both", expand=True)

        self.slider = tk.Scale(self, from_=0, to=1, resolution=0.05, orient=tk.HORIZONTAL, label="Threshold", command=lambda v: self.action())
        self.slider.set(0.3)
        self.slider.pack(side="bottom", fill="x", padx=10, pady=10)

    
    def update(self, items):
        for item in items:
            text = f'{item["class_name"]} {item["score"]:.2f}'
            self.listbox.insert(tk.END, text)

    def reset(self):
        self.listbox.delete(0, tk.END)
