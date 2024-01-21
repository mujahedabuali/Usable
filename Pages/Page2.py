
#for make a Web filter page
import customtkinter as ck
from PIL import Image
from db import mycursor,mydb


class page2(ck.CTkFrame):
    
    def toggle_checkbox(self,checkbox_number):
        current_state = self.checkbox_vars[checkbox_number].get()
        self.checkbox_vars[checkbox_number].set( current_state)
        if checkbox_number==0:
            if(current_state):
                sql = "INSERT INTO content (name,username) VALUES ('Social Networking',%s);"
                mycursor.execute(sql,(self.entered_username,))
            else:
                sql = "DELETE FROM content WHERE name = 'Social Networking' and username=%s"
                mycursor.execute(sql,(self.entered_username,))
        elif checkbox_number==2:
            if(current_state):
                sql = "INSERT INTO content (name,username) VALUES ('Adult and Pornography',%s);"
                mycursor.execute(sql,(self.entered_username,))
            else:
                sql = "DELETE FROM content WHERE name = 'Adult and Pornography' and username=%s"
                mycursor.execute(sql,(self.entered_username,))
        elif checkbox_number==1:
            if(current_state):
                sql = "INSERT INTO content (name,username) VALUES ('Streaming Media',%s);"
                mycursor.execute(sql,(self.entered_username,))
            else:
                sql = "DELETE FROM content WHERE name = 'Streaming Media' and username=%s"
                mycursor.execute(sql,(self.entered_username,))
        elif checkbox_number==3:
            if(current_state):
                sql = "INSERT INTO content (name,username) VALUES ('Games',%s);"
                mycursor.execute(sql,(self.entered_username,))
            else:
                sql = "DELETE FROM content WHERE name = 'Games' and username=%s"
                mycursor.execute(sql,(self.entered_username,))
        mydb.commit()    

    def __init__(self, parent,login_page_instance):
        self.login_page_instance = login_page_instance
        self.entered_username = self.login_page_instance.get_entered_username()

        mycursor.execute("SELECT name FROM content WHERE username = %s", (self.entered_username,))
        mycontent = mycursor.fetchall()
        self.checkbox_vars = [ck.BooleanVar() for _ in range(5)]
        for x in mycontent:
            if x==('Social Networking',):
                self.checkbox_vars[0]=ck.BooleanVar(value=True)
            elif x==('Adult and Pornography',):
                self.checkbox_vars[2]=ck.BooleanVar(value=True)
            elif x==('Games',):
                self.checkbox_vars[3]=ck.BooleanVar(value=True)
            elif x==('Streaming Media',):
                self.checkbox_vars[1]=ck.BooleanVar(value=True)

        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=10)

        self.filter_image = ck.CTkImage(Image.open("imags/filter.png"),size=(30,30))
        self.label = ck.CTkLabel(self, text=" Web Filter",image=self.filter_image,compound="left",corner_radius=20,height=50,font=ck.CTkFont(family="Times New Roman", size=25,weight="bold")) 
        self.label.pack(pady=15)

        self.label = ck.CTkLabel(self, text=" Choose what you want to filter:",corner_radius=40,height=50,font=("TkDefaultFont", 21, "underline")) 
        self.label.pack(pady=15)

        checkbox1 = ck.CTkCheckBox(self,text=' Social Media',variable=self.checkbox_vars[0], command=lambda:self.toggle_checkbox(0),font=("Times New Roman", 18)) 
        checkbox1.pack(pady=30,padx=10) 

        checkbox2 = ck.CTkCheckBox(self,text='    Movies',variable=self.checkbox_vars[1], command=lambda:(self.toggle_checkbox(1)),font=("Times New Roman", 18)) 
        checkbox2.pack(pady=30,padx=10) 

        checkbox3 = ck.CTkCheckBox(self,text='    Site +18',variable=self.checkbox_vars[2], command=lambda:(self.toggle_checkbox(2)),font=("Times New Roman", 18)) 
        checkbox3.pack(pady=30,padx=10) 

        checkbox4 = ck.CTkCheckBox(self,text='    Games',variable=self.checkbox_vars[3], command=lambda:(self.toggle_checkbox(3)),font=("Times New Roman", 18)) 
        checkbox4.pack(pady=30,padx=10) 

