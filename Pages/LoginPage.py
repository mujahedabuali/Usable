import customtkinter as customtkinter
from PIL import Image
from db import mycursor, mydb
import hashlib
import smtplib
from email.mime.text import MIMEText
import random
import string
import uuid

class login_page(customtkinter.CTkFrame):
    
    def __init__(self, parent,login):
        self.actionLogin = login
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        
        self.logo_image = customtkinter.CTkImage(Image.open("imags/security.png"),size=(40,40))
        self.signUp_image = customtkinter.CTkImage(Image.open("imags/add-friend.png"),size=(30,30))

        label = customtkinter.CTkLabel(self,text="Safe Web - Login  ",image=self.logo_image,compound="right",corner_radius=20,font=customtkinter.CTkFont(family="Times New Roman", size=30,weight="bold")) 
        label.pack(pady=60) 

        self.user_entry = customtkinter.CTkEntry(self, placeholder_text="Username", width=200)
        self.user_entry.pack(pady=30, padx=10)

        self.user_pass = customtkinter.CTkEntry(self, placeholder_text="Password", width=200, show="*")
        self.user_pass.pack(pady=20, padx=10) 

        button = customtkinter.CTkButton(self,text='Login',command=self.login) 
        button.pack(pady=0,padx=10) 

        self.label_phone=customtkinter.CTkLabel(self,text="Forget Password ",cursor="hand2",height=30,font=("TkDefaultFont", 12, "underline"))
        self.label_phone.pack(pady=0)

        checkbox = customtkinter.CTkCheckBox(self,text='Remember Me') 
        checkbox.pack(pady=15,padx=10) 

        self.label_message = customtkinter.CTkLabel(self, text="", text_color="red")
        self.label_message.pack(pady=10)
        


        self.label_SignUP=customtkinter.CTkLabel(self,text="    SIGN UP   ",cursor="hand2",image=self.signUp_image,compound="right",height=30,font=("TkDefaultFont", 22, "underline"))
        self.label_SignUP.pack(pady=10)

        self.label_SignUP.bind("<Button-1>", self.signUp)
        self.label_phone.bind("<Button-1>", self.open_forgot_password_window)

    def open_forgot_password_window(self, event):
        forgot_password_window = customtkinter.CTkToplevel(self)
        forgot_password_window.title("Forgot Password")
        customtkinter.set_appearance_mode("Dark")
        forgot_password_window.geometry("500x350")
        
        center_x = int(700)
        center_y = int(400)
        forgot_password_window.geometry(f"+{center_x}+{center_y}")

        mainLabel = customtkinter.CTkLabel(forgot_password_window,text="  Forget Password Page  ",cursor="hand2",image=self.signUp_image,compound="right",height=30,font=("Times New Roman", 25))
        mainLabel.pack(pady=10)

        label = customtkinter.CTkLabel(forgot_password_window, text="Your Email:",font=("TkDefaultFont", 16))
        label.pack(pady=10)

        email_entry = customtkinter.CTkEntry(forgot_password_window)
        email_entry.pack(pady=10)

        
        def ver():
            email = email_entry.get()
            verify_code = self.send_verification_code(email)  
            self.vertfic(verify_code)
            forgot_password_window.destroy()

        send_button = customtkinter.CTkButton(forgot_password_window,text='Send',command=ver) 
        send_button.pack(pady=0,padx=10)

    def signUp(self, event):
        signUp = customtkinter.CTkToplevel(self)
        signUp.title("sign Up")
        customtkinter.set_appearance_mode("Dark")
        signUp.geometry("800x750")
        
        center_x = int(600)
        center_y = int(220)
        signUp.geometry(f"+{center_x}+{center_y}")

        mainLabel = customtkinter.CTkLabel(signUp,text="  SIGN UP Page  ",cursor="hand2",image=self.signUp_image,compound="right",height=30,font=("Times New Roman", 25))
        mainLabel.pack(pady=10)
        
        label1 = customtkinter.CTkLabel(signUp, text="Email:",font=("TkDefaultFont", 16))
        label1.pack(pady=10)

        email_entry = customtkinter.CTkEntry(signUp, width=200)
        email_entry.pack(pady=10)

        label2 = customtkinter.CTkLabel(signUp, text="Phone Number:",font=("TkDefaultFont", 16))
        label2.pack(pady=10)

        phone_entry = customtkinter.CTkEntry(signUp, width=200)
        phone_entry.pack(pady=10)

        label = customtkinter.CTkLabel(signUp, text="User name:",font=("TkDefaultFont", 16))
        label.pack(pady=10)

        name_entry = customtkinter.CTkEntry(signUp, width=200)
        name_entry.pack(pady=10)

        label3 = customtkinter.CTkLabel(signUp, text="Strong Password:",font=("TkDefaultFont", 16))
        label3.pack(pady=10)

        pass_entry = customtkinter.CTkEntry(signUp, width=200, show="*")
        pass_entry.pack(pady=10)

        label4 = customtkinter.CTkLabel(signUp, text="Re-Enter Password:",font=("TkDefaultFont", 16))
        label4.pack(pady=10)

        pass_entry2 = customtkinter.CTkEntry(signUp, width=200, show="*")
        pass_entry2.pack(pady=10)

        label5 = customtkinter.CTkLabel(signUp, text="Mac Address:",font=("TkDefaultFont", 16))
        label5.pack(pady=10)

        mac_entry = customtkinter.CTkEntry(signUp, width=200)
        mac_entry.pack(pady=10)

        Unvalidlabel = customtkinter.CTkLabel(signUp, text="",font=("TkDefaultFont", 14), text_color="red")
        Unvalidlabel.pack(pady=10)

        def submit():
            # Check if the passwords match
            if pass_entry.get() != pass_entry2.get():
                Unvalidlabel.configure(text="Passwords do not match.")
                return

            entered_username = name_entry.get()

            # Check if the username already exists
            mycursor.execute("SELECT * FROM userdata WHERE username = %s", (entered_username,))
            existing_user = mycursor.fetchone()

            if existing_user:
                Unvalidlabel.configure(text="Username already exists. Please choose a different one.")
            else:
                verify_code = self.send_verification_code(email_entry.get())  
                hashed_password = hashlib.sha256(pass_entry.get().encode()).hexdigest()
                self.signup_vertfic(verify_code,entered_username,hashed_password,email_entry.get(),phone_entry.get(),mac_entry.get())
                signUp.destroy()

        submit_button = customtkinter.CTkButton(signUp, text="Submit", command=submit)
        submit_button.pack(pady=10)         

    def login(self): 
        # print(self.get_mac_address())
        entered_username = self.user_entry.get()
        entered_password = hashlib.sha256(self.user_pass.get().encode()).hexdigest()
        mycursor.execute("SELECT * FROM userdata WHERE username = %s AND password = %s", (entered_username, entered_password))
        result = mycursor.fetchone()
        mycursor.execute("SELECT email FROM userdata WHERE username = %s AND password = %s", (entered_username, entered_password))
        result1 = mycursor.fetchone()
        # mycursor.execute("SELECT macAddress FROM userdata WHERE username = %s AND password = %s", (entered_username, entered_password))
        # mac_address_tuple = mycursor.fetchone()

        # stored_mac_address = mac_address_tuple[0]
        # entered_mac_address = self.get_mac_address()
        # print(stored_mac_address)

        # if stored_mac_address == entered_mac_address :
        if result and result1:
                self.label_message.configure(text="")
                target_username = "entered_username"
                email = result1[0]
                verification_code = self.send_verification_code(email)  
                self.vertfic(verification_code,entered_username)

         
        else:
                self.label_message.configure(text="Invalid Username or Password")
        # else:
        #     self.label_message.configure(text="Invalid macAdress")

       
     
    def vertfic(self,verification_code,entered_username):
        ver = customtkinter.CTkToplevel(self)
        ver.title(" Vertfication Page")
        customtkinter.set_appearance_mode("Dark")
        ver.geometry("350x250")
        
        center_x = int(700)
        center_y = int(400)
        ver.geometry(f"+{center_x}+{center_y}")

        mainLabel = customtkinter.CTkLabel(ver,text="  Vertfication Page  ",cursor="hand2",height=30,font=("Times New Roman", 25))
        mainLabel.pack(pady=10)
        
        label1 = customtkinter.CTkLabel(ver, text="Code on you Email:",font=("TkDefaultFont", 16))
        label1.pack(pady=7)

        email_entry = customtkinter.CTkEntry(ver)
        email_entry.pack(pady=5)

        Wronglabel = customtkinter.CTkLabel(ver, text="",font=("TkDefaultFont", 14), text_color="red")
        Wronglabel.pack(pady=10)


        def check():
            entered_code = email_entry.get()

            if entered_code == verification_code:
                # Update the username in the lastuser table
                mycursor.execute("UPDATE lastuser SET username = %s WHERE id = 1", (entered_username,))

                # Commit the changes
                mydb.commit()
                ver.destroy()
                self.actionLogin()
            else:
                Wronglabel.configure(text="*Wrong Code")


        submit_button = customtkinter.CTkButton(ver, text="Submit", command=check )
        submit_button.pack(pady=10)  


    def signup_vertfic(self,verification_code,entered_username,hashed_password,email,phone,macAddress):
        ver1 = customtkinter.CTkToplevel(self)
        ver1.title(" Vertfication Page")
        customtkinter.set_appearance_mode("Dark")
        ver1.geometry("350x250")
        
        center_x = int(700)
        center_y = int(400)
        ver1.geometry(f"+{center_x}+{center_y}")

        mainLabel = customtkinter.CTkLabel(ver1,text="  Vertfication Page  ",cursor="hand2",height=30,font=("Times New Roman", 25))
        mainLabel.pack(pady=10)
        
        label1 = customtkinter.CTkLabel(ver1, text="Code on you Email:",font=("TkDefaultFont", 16))
        label1.pack(pady=7)

        email_entry = customtkinter.CTkEntry(ver1)
        email_entry.pack(pady=5)

        Wronglabel = customtkinter.CTkLabel(ver1, text="",font=("TkDefaultFont", 14), text_color="red")
        Wronglabel.pack(pady=10)


        def signup_check():
            entered_code = email_entry.get()

            if entered_code == verification_code:
                # Insert the new user into the userdata table
                sql = "INSERT INTO userdata (username, password, email, phonenumber, realtime_block, macAddress) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (entered_username, hashed_password, email, phone, False,macAddress)
                mycursor.execute(sql, values)
                mydb.commit()
                ver1.destroy()
            else:
                Wronglabel.configure(text="*Wrong Code")


        submit_button = customtkinter.CTkButton(ver1, text="Submit", command=signup_check )
        submit_button.pack(pady=10)


    def send_verification_code(self, email):
        # Generate a random verification code
        verification_code = ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit code

        self.verification_code = verification_code

        # Send the verification code via email
        subject = "Verification Code for Safe Web"
        body = f"Your verification code is: {verification_code}"
        sender_email = "adhamturki321@gmail.com"  # Replace with your email
        receiver_email = email

        # Use your SMTP server 
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_username = "adhamturki321@gmail.com"
        smtp_password = "hzaimilhhzljcgvn"

        # Create a message
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return verification_code

    

    def get_entered_username(self):
        return self.user_entry.get()
    def get_mac_address(self):
        # Get the MAC address of the first network interface
        try:
            mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
            return mac_address
        except Exception as e:
            print(f"Error obtaining MAC address: {e}")
            return None
