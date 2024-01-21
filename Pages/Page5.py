
#for make a Block site page
import customtkinter as ck
from PIL import Image
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from db import mycursor,mydb


class page5(ck.CTkFrame):
    def __init__(self, parent,login_page_instance):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

        self.login_page_instance = login_page_instance


        self.block_image = ck.CTkImage(Image.open("imags/ad.png"),size=(30,30))
        self.label = ck.CTkLabel(self, text=" Block Site",corner_radius=20,height=50,image=self.block_image,compound="left",font=ck.CTkFont(family="Times New Roman", size=25,weight="bold")) 
        self.label.pack(pady=5)
        
        columns = ('#1')
        self.table = ttk.Treeview(self,columns=columns,height=15, selectmode='browse',show='headings')

        self.table.column("#1", anchor="w",width=200,minwidth=200)
     
        self.table.heading('#1', text='URL')
        self.table.bind('<Motion>','break')

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, fieldbackground="Black")
        style.map("Treeview", background=[('selected', '#347083')])
        style.configure("Treeview", highlightthickness=0, bd=0)


        self.scrollbar = ck.CTkScrollbar(self, orientation=ck.VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side=ck.RIGHT, fill=ck.Y)

        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.table.pack(fill=ck.BOTH, expand=False,padx=15)


        button_frame = ck.CTkFrame(self,fg_color="transparent")
        button_frame.pack(fill=ck.BOTH, expand=False,padx=15,pady=20)

        self.add_button = ck.CTkButton(button_frame, text="Add new Block Site", command=self.add_data)
        self.add_button.place(x=200,y=100)

        self.edit_button = ck.CTkButton(button_frame, text="Edit a Block Site", command=self.edit_item)
        self.edit_button.place(x=400,y=100)

        self.delete_button = ck.CTkButton(button_frame, text="Delete a Block Site", command=self.delete_item)
        self.delete_button.place(x=600,y=100)
        self.entered_username = self.login_page_instance.get_entered_username()
        mycursor.execute("SELECT url FROM site WHERE username = %s", (self.entered_username,))
        mysite = mycursor.fetchall()
        for site in mysite:
            self.table.insert('','end',values=(site))


    def add_data(self):
        self.add_window()

    def add_window(self):

        def get():
            mycursor.execute("SELECT url FROM site WHERE username = %s", (self.entered_username,))
            mysite = mycursor.fetchall()
            if (self.entry.get()) :
                data = self.entry.get()
                if (data,) in mysite:
                    CTkMessagebox(title="Warning Message",message="This Url is already blocked",icon="warning",fade_in_duration=5)
                else:
                    sql = "INSERT INTO site (url,username) VALUES (%s,%s)"
                    mycursor.execute(sql, (data,self.entered_username))
                    mydb.commit()    
                    self.table.insert('','end',values=(data))
                    self.entry.delete(0,'end')

        new_window = ck.CTkToplevel(self)
        new_window.geometry("400x200")
        new_window.title('Add New Block Site')


        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        entry_label = ck.CTkLabel(new_window,width=200,text="Enter new URL:",font=ck.CTkFont(family="Times New Roman", size=18,weight="bold"))
        entry_label.pack(padx=10, pady=10)

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)

        ok_button = ck.CTkButton(new_window, text="OK", command=get)
        ok_button.pack(padx=10, pady=10)


    def edit_item(self):
         selected_item = self.table.focus()
         if selected_item:
            self.edit_window()
         else:  CTkMessagebox(title="Warning Message",message="Select a item Please",icon="warning",fade_in_duration=5)

    def edit_window(self):
        def get():
            if (self.entry.get()) :
                mycursor.execute("SELECT url FROM site WHERE username = %s", (self.entered_username,))
                mysite = mycursor.fetchall()
                if (self.entry.get()) :
                    data = self.entry.get()
                    if (data,) in mysite:
                        CTkMessagebox(title="Warning Message",message="This Url is already blocked",icon="warning",fade_in_duration=5)
                    else:
                        item = self.table.focus()
                        values = self.table.item(item, "values")
                        oldurl = values[0]
                        data = self.entry.get()
                        sql = "UPDATE site SET url = %s WHERE url = %s and username=%s"
                        mycursor.execute(sql, (data, oldurl,self.entered_username))
                        mydb.commit() 
                        self.table.item(item, values=data)
                        self.entry.delete(0,'end')

        new_window = ck.CTkToplevel(self)
        new_window.geometry("400x200")
        new_window.title('Edit Block Site')


        center_x = int(750)
        center_y = int(350)
        new_window.geometry(f"+{center_x}+{center_y}")

        entry_label = ck.CTkLabel(new_window,width=200,text="Enter new URL for Update :",font=ck.CTkFont(family="Times New Roman", size=18,weight="bold"))
        entry_label.pack(padx=10, pady=10)

        self.entry = ck.CTkEntry(new_window,width=200)
        self.entry.pack(padx=10, pady=10)

        ok_button = ck.CTkButton(new_window, text="OK", command=get)
        ok_button.pack(padx=10, pady=10)    

    def delete_item(self):
         selected_item = self.table.focus()
         if selected_item:
            values = self.table.item(selected_item, "values")
            oldurl = values[0]
            sql = "DELETE FROM  site  WHERE url = %s and username=%s"
            mycursor.execute(sql, (oldurl,self.entered_username))
            mydb.commit() 
            self.table.delete(selected_item)
         else:  CTkMessagebox(title="Warning Message",message="Select a item Please",icon="warning",fade_in_duration=5)

