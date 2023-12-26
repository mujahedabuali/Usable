
#for make a Web filter page
import customtkinter as ck
from PIL import Image



class page2(ck.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

        self.filter_image = ck.CTkImage(Image.open("imags/filter.png"),size=(30,30))
        self.label = ck.CTkLabel(self, text=" Web Filter",image=self.filter_image,compound="left",corner_radius=20,height=50,font=ck.CTkFont(family="Times New Roman", size=25,weight="bold")) 
        self.label.pack(pady=15)

        self.label = ck.CTkLabel(self, text=" Choose what you want to filter:",corner_radius=40,height=50,font=("TkDefaultFont", 21, "underline")) 
        self.label.pack(pady=15)
        
        checkbox1 = ck.CTkCheckBox(self,text=' Non Secure Site',font=("Times New Roman", 18)) 
        checkbox1.pack(pady=30,padx=10) 

        checkbox2 = ck.CTkCheckBox(self,text='  Sensitive Photos',font=("Times New Roman", 18)) 
        checkbox2.pack(pady=30,padx=10) 

        checkbox3 = ck.CTkCheckBox(self,text='   Untruted links',font=("Times New Roman", 18)) 
        checkbox3.pack(pady=30,padx=10) 

        checkbox4 = ck.CTkCheckBox(self,text='    Site +18',font=("Times New Roman", 18)) 
        checkbox4.pack(pady=30,padx=10) 

        checkbox5 = ck.CTkCheckBox(self,text='    Games',font=("Times New Roman", 18)) 
        checkbox5.pack(pady=30,padx=10) 

        checkbox6 = ck.CTkCheckBox(self,text='    Movies',font=("Times New Roman", 18)) 
        checkbox6.pack(pady=30,padx=10) 