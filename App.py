import customtkinter
from PIL import Image

from Pages.LoginPage import login_page
from Pages.Page2 import page2
from Pages.Page3 import page3
from Pages.Page4 import page4
from Pages.Page5 import page5
from Pages.settingPage import Setting_Page

#for make a taps on menu
class menuFrame(customtkinter.CTkFrame):
    def __init__(self, parent, page2, page3, page4,page5,setting,logout):
        super().__init__(parent, corner_radius=0)
        self.grid_rowconfigure(6, weight=1)

        self.logo_image = customtkinter.CTkImage(Image.open("imags/security.png"),size=(40,40))
        self.label = customtkinter.CTkLabel(self, text="  Safe Web Navigation",image=self.logo_image, compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.block_image = customtkinter.CTkImage(Image.open("imags/ad.png"),size=(20,20))
        self.bookmark_image = customtkinter.CTkImage(Image.open("imags/bookmark.png"),size=(20,20))
        self.filter_image = customtkinter.CTkImage(Image.open("imags/filter.png"),size=(20,20))
        self.hide_image = customtkinter.CTkImage(Image.open("imags/hide-and-seek.png"),size=(20,20))
        self.setting_image = customtkinter.CTkImage(Image.open("imags/settings.png"),size=(20,20))

        self.page5_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Site Blocking",image=self.block_image, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=page5)
        self.page5_button.grid(row=1, column=0, sticky="ew")

        self.page2_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Web Filtering", image=self.filter_image, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=page2)
        self.page2_button.grid(row=2, column=0, sticky="ew")

        self.page3_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Book Marks Save", image=self.bookmark_image, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=page3)
        self.page3_button.grid(row=4, column=0, sticky="ew")

        self.page4_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="History Hiding", image=self.hide_image, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=page4)
        self.page4_button.grid(row=3, column=0, sticky="ew")


        self.setting_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Settings",image=self.setting_image, compound="left",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=setting)
        self.setting_button.grid(row=5, column=0, sticky="ew")

        self.logout_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Log out", fg_color="transparent", text_color=("red", "red"), hover_color=("gray70", "gray30"), anchor="w",command=logout)
        self.logout_button.grid(row=7, column=0, sticky="ew")

#Drive class
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("Dark")

        self.title("SAFE WEB NAVIGATION")
        self.geometry("1200x800")
        center_x = int(350)
        center_y = int(100)
        self.geometry(f"+{center_x}+{center_y}")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.loginPage=login_page(self,self.login)
        self.loginPage.grid(row=0, column=1, sticky="nsew")

        self.navigation_frame = menuFrame(self, self.page2_event, self.page3_event, self.page4_event,self.page5_event,self.setting_event,self.logout)
        
        self.page2 = page2(self)#web filter
        self.page3 = page3(self)#book mark
        self.page4 = page4(self)#book mark
        self.page5 = page5(self)#Block site
        self.sett_Page= Setting_Page(self)#Setting Page


    def select_frame_by_name(self, name):
        self.navigation_frame.page2_button.configure(fg_color=("gray75", "gray25") if name == "page2" else "transparent")
        self.navigation_frame.page3_button.configure(fg_color=("gray75", "gray25") if name == "page3" else "transparent")
        self.navigation_frame.page4_button.configure(fg_color=("gray75", "gray25") if name == "page4" else "transparent")
        self.navigation_frame.page5_button.configure(fg_color=("gray75", "gray25") if name == "page5" else "transparent")
        self.navigation_frame.setting_button.configure(fg_color=("gray75", "gray25") if name == "Setting" else "transparent")

        self.page2.grid_remove()
        self.page3.grid_remove()
        self.page4.grid_remove()
        self.page5.grid_remove()
        self.sett_Page.grid_remove()
        if name == "page2":
            self.page2.grid(row=0, column=1, sticky="nsew")
       

        elif name == "page3":
            self.page3.grid(row=0, column=1, sticky="nsew")
      

        elif name == "page4":
            self.page4.grid(row=0, column=1, sticky="nsew")
      
        elif name == "page5":
            self.page5.grid(row=0, column=1, sticky="nsew")


        elif name == "Setting":
            self.sett_Page.grid(row=0, column=1, sticky="nsew")
  
        self.update_idletasks()         


    def login(self):
       self.navigation_frame.grid(row=0, column=0, sticky="nsew")
       self.select_frame_by_name("page5")
       self.loginPage.grid_forget()

    def logout(self):
       self.navigation_frame.grid_forget()
       self.page2.grid_forget()
       self.page4.grid_forget()
       self.page3.grid_forget()
       self.page5.grid_forget()
       self.sett_Page.grid_forget()
       self.loginPage.grid(row=0, column=1, sticky="nsew")
       self.update_idletasks()         

    

    def page2_event(self):
        self.select_frame_by_name("page2")

    def page3_event(self):
        self.select_frame_by_name("page3")

    def page4_event(self):
        self.select_frame_by_name("page4")    

    def page5_event(self):
        self.select_frame_by_name("page5") 
   
    def setting_event(self):
        self.select_frame_by_name("Setting")       


if __name__ == "__main__":
    app = App()
    app.mainloop()
