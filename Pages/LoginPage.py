import customtkinter as customtkinter
from PIL import Image

class login_page(customtkinter.CTkFrame):
    def __init__(self, parent,login):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        
        self.logo_image = customtkinter.CTkImage(Image.open("imags/security.png"),size=(40,40))
        label = customtkinter.CTkLabel(self,text="Safe Web - Login  ",image=self.logo_image,compound="right",corner_radius=20,height=50,font=customtkinter.CTkFont(family="Times New Roman", size=25,weight="bold")) 
        label.pack(pady=60) 

        user_entry= customtkinter.CTkEntry(self,placeholder_text="Username",width=200) 
        user_entry.pack(pady=30,padx=10) 

        user_pass= customtkinter.CTkEntry(self,placeholder_text="Password",width=200,show="*") 
        user_pass.pack(pady=20,padx=10) 

        button = customtkinter.CTkButton(self,text='Login',command=login) 
        button.pack(pady=0,padx=10) 

        label_phone=customtkinter.CTkLabel(self,text="Forget Password ",cursor="hand2",height=30,font=("TkDefaultFont", 12, "underline"))
        label_phone.pack(pady=0)

        checkbox = customtkinter.CTkCheckBox(self,text='Remember Me') 
        checkbox.pack(pady=30,padx=10) 

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

