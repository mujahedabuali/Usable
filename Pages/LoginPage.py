import customtkinter as customtkinter
from PIL import Image

class login_page(customtkinter.CTkFrame):
    def __init__(self, parent,login):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        
        self.logo_image = customtkinter.CTkImage(Image.open("imags/security.png"),size=(40,40))
        self.signUp_image = customtkinter.CTkImage(Image.open("imags/add-friend.png"),size=(30,30))

        label = customtkinter.CTkLabel(self,text="Safe Web - Login  ",image=self.logo_image,compound="right",corner_radius=20,font=customtkinter.CTkFont(family="Times New Roman", size=30,weight="bold")) 
        label.pack(pady=60) 

        user_entry= customtkinter.CTkEntry(self,placeholder_text="Username",width=200) 
        user_entry.pack(pady=30,padx=10) 

        user_pass= customtkinter.CTkEntry(self,placeholder_text="Password",width=200,show="*") 
        user_pass.pack(pady=20,padx=10) 

        button = customtkinter.CTkButton(self,text='Login',command=login) 
        button.pack(pady=0,padx=10) 

        self.label_phone=customtkinter.CTkLabel(self,text="Forget Password ",cursor="hand2",height=30,font=("TkDefaultFont", 12, "underline"))
        self.label_phone.pack(pady=0)

        checkbox = customtkinter.CTkCheckBox(self,text='Remember Me') 
        checkbox.pack(pady=15,padx=10) 

        self.label_SignUP=customtkinter.CTkLabel(self,text="    SIGN UP   ",cursor="hand2",image=self.signUp_image,compound="right",height=30,font=("TkDefaultFont", 22, "underline"))
        self.label_SignUP.pack(pady=150)

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

        label2 = customtkinter.CTkLabel(forgot_password_window, text="Your Phone Number:",font=("TkDefaultFont", 16))
        label2.pack(pady=10)

        phone_entry = customtkinter.CTkEntry(forgot_password_window)
        phone_entry.pack(pady=10)


        submit_button = customtkinter.CTkButton(forgot_password_window, text="Submit", command=lambda: self.submit_email(email_entry.get()))
        submit_button.pack(pady=10)

    def signUp(self, event):
        signUp = customtkinter.CTkToplevel(self)
        signUp.title("sign Up")
        customtkinter.set_appearance_mode("Dark")
        signUp.geometry("700x650")
        
        center_x = int(600)
        center_y = int(220)
        signUp.geometry(f"+{center_x}+{center_y}")

        mainLabel = customtkinter.CTkLabel(signUp,text="  SIGN UP Page  ",cursor="hand2",image=self.signUp_image,compound="right",height=30,font=("Times New Roman", 25))
        mainLabel.pack(pady=10)
        
        label1 = customtkinter.CTkLabel(signUp, text="Email:",font=("TkDefaultFont", 16))
        label1.pack(pady=10)

        email_entry = customtkinter.CTkEntry(signUp)
        email_entry.pack(pady=10)

        label2 = customtkinter.CTkLabel(signUp, text="Phone Number:",font=("TkDefaultFont", 16))
        label2.pack(pady=10)

        phone_entry = customtkinter.CTkEntry(signUp)
        phone_entry.pack(pady=10)

        label = customtkinter.CTkLabel(signUp, text="User name:",font=("TkDefaultFont", 16))
        label.pack(pady=10)

        name_entry = customtkinter.CTkEntry(signUp)
        name_entry.pack(pady=10)

        label3 = customtkinter.CTkLabel(signUp, text="Strong Password:",font=("TkDefaultFont", 16))
        label3.pack(pady=10)

        pass_entry = customtkinter.CTkEntry(signUp)
        pass_entry.pack(pady=10)

        label4 = customtkinter.CTkLabel(signUp, text="Re-Enter Password:",font=("TkDefaultFont", 16))
        label4.pack(pady=10)

        pass_entry2 = customtkinter.CTkEntry(signUp)
        pass_entry2.pack(pady=10)


        submit_button = customtkinter.CTkButton(signUp, text="Submit", command=lambda: self.submit_email(email_entry.get()))
        submit_button.pack(pady=10)         

    def login(): 

        username = "1"
        password = "1"
        # new_window = ctk.CTkToplevel(app) 

        # new_window.title("New Window") 

        # new_window.geometry("350x150") 

        # if user_entry.get() == username and user_pass.get() == password: 
        #     tkmb.showinfo(title="Login Successful",message="You have logged in Successfully") 
        #     ctk.CTkLabel(new_window,text="GeeksforGeeks is best for learning ANYTHING !!").pack() 
        # elif user_entry.get() == username and user_pass.get() != password: 
        #     tkmb.showwarning(title='Wrong password',message='Please check your password') 
        # elif user_entry.get() != username and user_pass.get() == password: 
        #     tkmb.showwarning(title='Wrong username',message='Please check your username') 
        # else: 
        #     tkmb.showerror(title="Login Failed",message="Invalid Username and password") 

