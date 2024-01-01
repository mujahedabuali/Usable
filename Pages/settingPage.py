
#for make a Web filter page
import customtkinter as ck
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from PIL import Image

class Setting_Page(ck.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

        self.setting_image = ck.CTkImage(Image.open("imags/settings.png"),size=(30,30))
        self.label = ck.CTkLabel(self, text=" Settings",corner_radius=20,height=50,image=self.setting_image,compound="left",font=ck.CTkFont(family="Times New Roman", size=25,weight="bold")) 
        self.label.place(x=410,y=15)

        # Labels
        ck.CTkLabel(self, text="Username:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold")).place(x=320,y=120)
        ck.CTkLabel(self, text="Password:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold")).place(x=320,y=200)
        ck.CTkLabel(self, text="Re-Enter Password:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold")).place(x=320,y=280)
        ck.CTkLabel(self, text="Email:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold")).place(x=320,y=360)
        ck.CTkLabel(self, text="Phone Number:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold")).place(x=320,y=440)

        # Entry widgets
        self.username_entry = ck.CTkEntry(self)
        self.password_entry = ck.CTkEntry(self, show="*")
        self.password_entry2 = ck.CTkEntry(self, show="*")
        self.email_entry = ck.CTkEntry(self)
        self.phone_entry = ck.CTkEntry(self)

        self.username_entry.place(x=490,y=120)
        self.password_entry.place(x=490,y=200)
        self.password_entry2.place(x=490,y=280)
        self.email_entry.place(x=490,y=360)
        self.phone_entry.place(x=490,y=440)
        
         # Save button
        save_button = ck.CTkButton(self, text="Save Changes", command=self.save_changes)
        save_button.place(x=420,y=500)

    def save_changes(self):
        # Get values from entry widgets
        new_username = self.username_entry.get()
        new_password = self.password_entry.get()
        new_password2 = self.password_entry2.get()
        new_email = self.email_entry.get()
        new_phone = self.phone_entry.get()

        if new_username and new_password and new_email and new_phone and new_password2 and (new_password2 == new_password):
            CTkMessagebox(title="Success Message",message="Changes saved successfully!",icon="info",fade_in_duration=5)
        else:
            CTkMessagebox(title="Error",message="Check all filed or Password not Similar",icon="cancel",fade_in_duration=5)

    
