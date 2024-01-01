
#for make a Histroy Hiding page
import customtkinter as ck
from PIL import Image
from tkinter import ttk
from CTkMessagebox import CTkMessagebox


class page4(ck.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

        self.bookmark_image = ck.CTkImage(Image.open("imags/hide-and-seek.png"),size=(30,30))
        self.label = ck.CTkLabel(self, text=" Histroy Hiding",image=self.bookmark_image,corner_radius=20,compound="left",height=50,font=ck.CTkFont(family="Times New Roman", size=25,weight="bold")) 
        self.label.pack(pady=5)
        
        columns = ('#1')
        self.table = ttk.Treeview(self,columns=columns,height=15, selectmode='browse',show='headings')

        self.table.column("#1", anchor="w",width=100,minwidth=100)
     
        self.table.heading('#1', text='URL')
        self.table.bind('<Motion>','break')

        self.scrollbar = ck.CTkScrollbar(self, orientation=ck.VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side=ck.RIGHT, fill=ck.Y)

        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.table.pack(fill=ck.BOTH, expand=False,padx=15)

        self.delete_button = ck.CTkButton(self, text="Delete All Histroy", command=self.delete_item(self.table))
        self.delete_button.place(x=410,y=600)

    def delete_item(self,tree):
         self.table.delete(*tree.get_children())

