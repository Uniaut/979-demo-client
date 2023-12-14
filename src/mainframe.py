import enum

import tkinter as tk
import cv2

from src.sections import WebcamContentSection, DetectedItemsSection
from src.utils import request_prediction, visualize, to_items


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

        self.description = tk.Label(self.header, text="Capturing and detecting Fashionpedia-trained fashion objects.", wraplength=400)
        self.description.pack(side="top", pady=5)

        self.content = tk.Frame(self)
        self.content.pack(fill="both", expand=True)

        self.webcam_content = WebcamContentSection(self.content, action=self.action)
        self.webcam_content.pack(side="left", fill="both", padx= 10, pady= 5, expand=True)

        self.detected_items = DetectedItemsSection(self.content, action=self.visualize_with_threshold)
        self.detected_items.pack(side="right", fill="both", padx= 10, pady= 5, expand=True)

        self.preview()
    
    
    def preview(self):
        if self.mode == Mode.PREVIEW:
            self.webcam_content.update_preview()
            self.content.after(20, self.preview)


    def capture_and_predict(self):
        self.mode = Mode.PREDICTED
        frame = self.webcam_content.update_preview()
        
        # resize the frame 75% smaller
        frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)

        rois, class_ids, scores = request_prediction(frame)

        self.results = (frame, rois, class_ids, scores)

        self.visualize_with_threshold()
        
        items = to_items(rois, class_ids, scores)
        self.detected_items.update(items)

    
    def visualize_with_threshold(self):
        frame, rois, class_ids, scores = self.results
        image = visualize(frame, rois, class_ids, scores, self.detected_items.slider.get())
        self.webcam_content.update_predicted(image)




    def action(self):
        if self.mode == Mode.PREVIEW:
            self.after(3000, self.capture_and_predict)
            self.webcam_content.action_button.configure(state="active", text="Reset")
        else:
            self.mode = Mode.PREVIEW
            self.webcam_content.action_button.configure(state="active", text="Capture")
            self.detected_items.reset()
            self.preview()
