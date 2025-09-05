import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox
import customtkinter as ctk

folder_path = "D:/Git Repository/FaceAttendanceSystem/FaceAttendance/data/"

class App(ctk.CTk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')

        self.main = Main(self, 'gray')
        self.main.create_widgets()
        self.label = self.main.label
        self.main.button.configure(command=self.create_user_window)

        #camera
        self.cap = cv2.VideoCapture(0)
        self.update()
        self.access_camera()

        self.mainloop()

    def access_camera(self):
            _, frame = self.cap.read()
            self.imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.most_recent_capture = Image.fromarray(self.imgRGB)
            self.resized_img = Image.fromarray(self.imgRGB).resize((self.label.winfo_width() - 4, self.label.winfo_height() - 4))
            self.imgTK = ImageTk.PhotoImage(self.resized_img)

            #Set Image To The Label
            self.label.imgtk = self.imgTK
            self.label.configure(image=self.imgTK)

            #Recall Function
            self.label.after(20, self.access_camera)
    
    def create_user_window(self):
        global imgArray, canCreateWindow
        imgArray = self.imgRGB
        canCreateWindow = True
        self.destroy()

class Main(ctk.CTkFrame):
    def __init__(self, parent, label_bg):
        super().__init__(parent)
        self.label_bg = label_bg
        self.pack(expand=True, fill='both')
    
    def create_widgets(self):
        self.label = ctk.CTkLabel(self, fg_color=self.label_bg, text="")
        self.label.place(relx=0.02, rely=0.02, relwidth=0.65, relheight=0.96)

        self.button = ctk.CTkButton(self, text="Register New User")
        self.button.place(relx=0.834, rely=0.5, relwidth=0.2, relheight=0.1, anchor='center')

class Secondary(ctk.CTk):
    def __init__(self, title, size):
        super().__init__()
        self.win_title = title
        self.win_size = size
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')

        Details(self, imgArray)

        self.mainloop()

class Details(ctk.CTkFrame):
    def __init__(self, parent, image):
        super().__init__(parent)
        self.parent = parent
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.image = Image.fromarray(image)
        self.imgPIL = self.image
        self.create_widgets()
        
    def change_image_size(self):
            imgPIL = self.imgPIL.resize((self.label.winfo_width() - 4, self.label.winfo_height() - 4))
            imgTk = ImageTk.PhotoImage(imgPIL)
            self.label.imgtk = imgTk
            self.label.configure(image=imgTk)
            self.label.after(20, self.change_image_size)
    def create_widgets(self):
        self.name_string = tk.StringVar()

        self.label = ttk.Label(self, background='gray')
        self.label.place(relx=0.02, rely=0.02, relwidth=0.65, relheight=0.96)
        self.update()
        self.change_image_size()

        self.side_panel = ctk.CTkFrame(self)
        self.side_panel.columnconfigure((0, 1, 2), weight=1, uniform='a')
        self.side_panel.rowconfigure((0, 1, 2), weight=1, uniform='a')

        name = ctk.CTkLabel(self.side_panel, text="Enter Your Name:", font=("Jokerman", 20))
        name.grid(row=0, column=0, columnspan=3)

        entry = ctk.CTkEntry(self.side_panel, textvariable=self.name_string)
        entry.grid(row=1, column=0, columnspan=3, sticky='ew')

        accept = ctk.CTkButton(self.side_panel, text="Confirm", command=self.save_image)
        accept.grid(row=2, column=0, sticky='ew')

        retry = ctk.CTkButton(self.side_panel, text="Retry", command=self.recreate_window)
        retry.grid(row=2, column=2, sticky='ew')

        self.side_panel.place(relx=0.83, rely=0.5, relwidth=0.3, relheight=0.6, anchor='center')
    def recreate_window(self):
        global recreateWindow
        recreateWindow = True
        self.parent.destroy()
    
    def save_image(self):
        if self.name_string.get() != "":
            messagebox.askokcancel("User Registered", f"User with name {self.name_string.get()} has been registered successfully")
            self.image.save(f'{folder_path}known_people/{self.name_string.get()}.jpg')
            self.parent.destroy()
        else:
            messagebox.askokcancel("Empty Name", "Please Enter A Valid Name.", icon='error')

if __name__ == "__main__":
    recreateWindow = True
    imgArray = None
    while recreateWindow:
        canCreateWindow = False
        app = App("Register User", (1000, 600))
        app.cap.release()
        if canCreateWindow:
            recreateWindow = False
            secondary = Secondary("Register New User", (1000, 600))
            if not recreateWindow:
                break
        else:
            break