import tkinter as tk
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('robotics_project/python/object_detection_model/best.pt')
# object classes
classNames = ['bear', 'fox', 'moose', 'santa']

class gui:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.video_source = 0  # default webcam index
        self.cap = cv2.VideoCapture(self.video_source)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.canvas = tk.Canvas(window, width=800, height=600)
        self.canvas.pack()
        
        self.btn_quit = tk.Button(window, text="Quit", width=10, command=self.quit_app)
        self.btn_quit.pack(pady=10)
        
        self.video()
        self.window.mainloop()
    
    def video(self):
        ret, frame = self.cap.read()
        results = model(frame, stream=True)
        if ret:
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                    # put box in cam
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                    # confidence
                    confidence = math.ceil((box.conf[0]*100))/100
                    print("Confidence --->",confidence)

                    # class name
                    cls = int(box.cls[0])
                    print("Class name -->", classNames[cls])

                    # object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2

                    cv2.putText(frame, classNames[cls], org, font, fontScale, color, thickness)

            resized_frame = cv2.resize(frame, (360, 240))  # Adjust width and height as needed
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(resized_frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.video)
    def quit_app(self):
        self.cap.release()
        self.window.destroy()

    
# Create a window and pass it to the VideoPlayerApp class
root = tk.Tk()
app = gui(root, "Slowly but surely")
