import tkinter as tk

from sections import WebcamContentSection, DetectedItemsSection


class Mainframe(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(highlightbackground="white", borderwidth=2, relief="solid")
        self.pack_propagate(False)

        self.header = tk.Frame(self)
        self.header.pack(fill="x", side="top")
        
        self.title = tk.Label(self.header, text="Object Detection Demo", font=("Arial", 18))
        self.title.pack(side="top", pady=10)

        self.description = tk.Label(self.header, text="This demo uses your webcam to detect objects in real-time.", wraplength=400)
        self.description.pack(side="top", pady=5)

        self.content = tk.Frame(self)
        self.content.pack(fill="both", expand=True)

        webcam_content = WebcamContentSection(self.content, action=lambda: print("action"))
        webcam_content.pack(side="left", fill="both", padx= 10, pady= 5, expand=True)

        detected_items = DetectedItemsSection(self.content)
        detected_items.pack(side="right", fill="both", padx= 10, pady= 5, expand=True)