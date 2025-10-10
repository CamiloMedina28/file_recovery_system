import customtkinter as ctk

class MainApp(ctk.CTkFrame):
    def __init__(self):
        super().__init__(self, fg_color = '')


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()