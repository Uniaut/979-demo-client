import enum

import tkinter as tk

from src.sections import WebcamContentSection, DetectedItemsSection
from src.utils import func


class Mode(enum.Enum):
    PREVIEW = 1
    CAPTURED = 2
    PREDICTED = 3


class Mainframe(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(highlightbackground="white", borderwidth=2, relief="solid")
        self.pack_propagate(False)
        self.mode = Mode.PREVIEW

        self.header = tk.Frame(self)
        self.header.pack(fill="x", side="top")
        
        self.title = tk.Label(self.header, text="Object Detection Demo", font=("Arial", 18))
        self.title.pack(side="top", pady=10)

        self.description = tk.Label(self.header, text="This demo uses your webcam to detect objects in real-time.", wraplength=400)
        self.description.pack(side="top", pady=5)

        self.content = tk.Frame(self)
        self.content.pack(fill="both", expand=True)

        self.webcam_content = WebcamContentSection(self.content, action=self.change_mode)
        self.webcam_content.pack(side="left", fill="both", padx= 10, pady= 5, expand=True)

        self.detected_items = DetectedItemsSection(self.content)
        self.detected_items.pack(side="right", fill="both", padx= 10, pady= 5, expand=True)

        self.preview()
    

    def update_prediction(self):
        self.webcam_content.update()
        self.detected_items.update()

    
    def preview(self):
        if self.mode == Mode.PREVIEW:
            self.webcam_content.update_preview()
            self.content.after(10, self.preview)


    def capture(self):
        self.webcam_content.update_preview()
    

    def change_mode(self):
        if self.mode == Mode.PREVIEW:
            self.capture()
            print('change mode to captured')
            self.mode = Mode.CAPTURED
            self.webcam_content.action_button.configure(state="disabled", text="Predicting...")
            func(self.change_mode)
        elif self.mode == Mode.CAPTURED:
            print('change mode to predicted')
            self.mode = Mode.PREDICTED
            self.webcam_content.action_button.configure(state="active", text="Reset")
        else:
            print('change mode to preview')
            self.mode = Mode.PREVIEW
            self.webcam_content.action_button.configure(state="active", text="Capture")
            self.preview()
