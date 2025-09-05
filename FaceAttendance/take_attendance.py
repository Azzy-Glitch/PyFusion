import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image
import customtkinter as ctk
import os
import face_recognition
import csv
from datetime import datetime
import win32com.client

folder_path = "D:/Git Repository/FaceAttendanceSystem/FaceAttendance/data/"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

speaker = win32com.client.Dispatch("SAPI.SpVoice")

class App(ctk.CTk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')

        self.label = ctk.CTkLabel(self, text="", bg_color="gray")
        self.label.place(relx=0.02, rely=0.02, relwidth=0.65, relheight=0.96)
        self.all_names = []
        self.name = ""

        self.load_folder = self.load_images_from_folder(f"{folder_path}known_people")

        ctk.CTkLabel(self, text="Recent Attendance", font=("Jokerman", 16), justify='center').place(relx=0.83, rely=0.32, relwidth=0.3, relheight=0.3, anchor='center')
        self.frame = ctk.CTkFrame(self, border_width=5)
        self.frame.place(relx=0.83, rely=0.5, relwidth=0.3, relheight=0.3, anchor='center')

        self.table = ttk.Treeview(self.frame, columns=("Name", "Time", "Role"), show="headings")

        #camera
        self.pic_timer = 0
        self.cap = cv2.VideoCapture(0)
        self.update()
        self.access_camera()

        self.mainloop()

    def access_camera(self):
            _, frame = self.cap.read()
            faces = face_cascade.detectMultiScale(frame, 1.3, 5)
            self.imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.most_recent_capture = Image.fromarray(self.imgRGB)
            self.imgTK = ctk.CTkImage(self.most_recent_capture, size=(self.label.winfo_width() - 4, self.label.winfo_height() - 4))

            #detect faces
            if len(faces) > 0:
                self.pic_timer += 1
                if self.pic_timer >= 20:
                    self.pic_timer = 0
                    self.take_attendance()

            #Set Image To The Label
            self.label.imgtk = self.imgTK
            self.label.configure(image=self.imgTK)

            #Recall Function
            self.label.after(20, self.access_camera)
    
    def recent(self):

        self.table.heading("Name", text="Name")
        self.table.heading("Time", text="Time")
        self.table.heading("Role", text="Role")

        self.table.column("Name", width=30)
        self.table.column("Time", width=30)
        self.table.column("Role", width=30)

        self.table.pack(expand=True, fill="both")

        self.table.insert(parent="", index=0, values=(self.name, self.time, self.role))

    def take_attendance(self):
        try:
            self.compare_image = self.most_recent_capture

            self.compare_image.save(f"{folder_path}unknown_people/recent_login.jpg")
            target_face_image = face_recognition.load_image_file(f"{folder_path}unknown_people/recent_login.jpg")
            target_face_encoding = face_recognition.face_encodings(target_face_image)[0]

            self.match = self.compare_faces(target_face_encoding)
            
            if self.match:
                image_name = self.image_name.split("-")
                if len(image_name) > 1:
                    self.name = image_name[0]
                    self.role = image_name[-1].capitalize()
                else:
                    self.name = image_name[0]
                    self.role = "Student"
                if self.name not in self.all_names:
                    self.all_names.append(self.name)
                    self.mark_attendance()
            else:
                self.name = "Unknown"
                self.time = datetime.now().strftime('%H-%M-%S')
                self.role = "Null"
                self.compare_image.save(f"{folder_path}unknown_people/{self.time}.jpg")
                self.recent()
        except:
            pass
    def load_images_from_folder(self, folder):
        encodings = []
        images = []
        for filename in os.listdir(folder):
            img_path = os.path.join(folder, filename)
            if os.path.isfile(img_path):
                img_path = img_path.replace("\\", "/")
                images.append(img_path)
                img = face_recognition.load_image_file(img_path)
                img_encoding = face_recognition.face_encodings(img)[0]
                encodings.append(img_encoding)
        return encodings, images
    
    def compare_faces(self, target_face_encoding):
        known_faces, images = self.load_folder

        for i, known_face_encoding in enumerate(known_faces):
            results = face_recognition.compare_faces([target_face_encoding], known_face_encoding, 0.4)
            if True in results:
                self.image_name = images[i].split("/")[-1].split(".")[0]
                return True
        
        return False

    def mark_attendance(self):
        date = datetime.now().strftime("%d-%m-%Y")
        self.time = datetime.now().strftime("%H-%M-%S")
        if os.path.exists(f"{folder_path}attendance_{date}.csv"):
            with open(f"{folder_path}attendance_{date}.csv", "a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([f"{self.name}", f"{self.time}", f"{self.role}"])
        else:
            with open(f"{folder_path}attendance_{date}.csv", "a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["NAME", "TIME", "ROLE"])
                writer.writerow([f"{self.name}", f"{self.time}", f"{self.role}"])
        if self.role.endswith("dent"):
            speaker.Speak("Attendance Marked")
        elif self.role.endswith("cher"):
            speaker.Speak(f"Good Morning Sir, your attendance has been marked")

        self.recent()

if __name__ == "__main__":
    app = App("Mark Attendance", (1100, 600))
    os.remove(f"{folder_path}unknown_people/recent_login.jpg")