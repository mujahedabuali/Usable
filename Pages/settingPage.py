
#for make a Web filter page
import customtkinter as ck
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from PIL import Image
from db import mycursor, mydb
import hashlib


class Setting_Page(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

        self.login_page_instance = login_page_instance



        self.setting_image = ck.CTkImage(Image.open("imags/settings.png"),size=(30,30))
        self.label = ck.CTkLabel(self, text=" Settings",corner_radius=20,height=50,image=self.setting_image,compound="left",font=ck.CTkFont(family="Times New Roman", size=25,weight="bold")) 
        self.label.place(x=410,y=15)

        # Labels
        ck.CTkLabel(self, text="Username:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold")).place(x=320,y=120)
        ck.CTkLabel(self, text="New Username:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold")).place(x=320,y=120)
        ck.CTkLabel(self, text="Password:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold")).place(x=320,y=200)
        ck.CTkLabel(self, text="Re-Enter Password:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold")).place(x=320,y=280)
        ck.CTkLabel(self, text="Email:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold")).place(x=320,y=360)
        ck.CTkLabel(self, text="Phone Number:",font=ck.CTkFont(family="Times New Roman", size=19,weight="bold")).place(x=320,y=440)

        # Entry widgets
        self.username_entry = ck.CTkEntry(self, width=200)
        self.new_username_entry = ck.CTkEntry(self, width=200)
        self.password_entry = ck.CTkEntry(self, show="*", width=200)
        self.password_entry2 = ck.CTkEntry(self, show="*", width=200)
        self.email_entry = ck.CTkEntry(self, width=200)
        self.phone_entry = ck.CTkEntry(self, width=200)

        self.username_entry.place(x=490,y=120)
        self.password_entry.place(x=490,y=200)
        self.password_entry2.place(x=490,y=280)
        self.email_entry.place(x=490,y=360)
        self.phone_entry.place(x=490,y=440)

        self.checkbox1 = ck.CTkCheckBox(self,text=' Real-Time Bloking',font=("Times New Roman", 18)) 
        self.checkbox1.place(x=400,y=600)
        
         # Save button
        save_button = ck.CTkButton(self, text="Save Changes", command=self.save_changes)
        save_button.place(x=420,y=500)
        # self.load_user_data()


    def save_changes(self):
        entered_username = self.login_page_instance.get_entered_username()

        # Get values from entry widgets
        new_username = self.username_entry.get()
        new_password = self.password_entry.get()
        new_password2 = self.password_entry2.get()
        new_email = self.email_entry.get()
        new_phone = self.phone_entry.get()
        realtime_block_value = True if self.checkbox1.get() else False


        # Check if all fields are not empty
        if not all([new_username, new_password, new_password2, new_email, new_phone]):
            CTkMessagebox(title="Failed Message", message="Please fill all the fields!", icon="info", fade_in_duration=5)
            return

        # Check if the password and re-entered password match
        if new_password != new_password2:
            CTkMessagebox(title="Failed Message",message="The two passwords are not matched!",icon="info",fade_in_duration=5)
            return

        # Update the user's information in the 'userdata' table
        update_query = """
        UPDATE userdata
        SET password = %s, email = %s, phonenumber = %s, realtime_block = %s, username = %s
        WHERE username = %s
        """

        # Hash the new password before updating
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        # Execute the update query
        mycursor.execute(update_query, (hashed_password, new_email, new_phone,realtime_block_value, new_username,entered_username))
        CTkMessagebox(title="Successful Message",message="Successfully changed!",icon="info",fade_in_duration=5)

        mydb.commit()

    # def load_user_data(self):
    #     # Fetch user data from the 'userdata' table based on the logged-in user's username
    #     user_name = self.login_page_instance.get_entered_username()
    #     print(user_name)
    #     select_query = "SELECT email, phonenumber FROM userdata WHERE username = %s"

    #     mycursor.execute(select_query, (user_name,))
    #     user_data = mycursor.fetchone()

    #     if user_data:
    #         self.email_entry.set(user_data[0])  # Index 0 corresponds to email in the query
    #         self.phone_entry.set(user_data[1])  # Index 1 corresponds to phonenumber in the query

        
    
