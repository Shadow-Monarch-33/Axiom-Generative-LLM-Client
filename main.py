import customtkinter as ctk

from database import setup_database
from ui.login import LoginFrame
from ui.signup import SignupFrame
from ui.chat import ChatFrame

ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):

        super().__init__()

        # Window settings

        self.title("AURA")
        self.geometry("900x650")
        self.minsize(700, 550)
        self.configure(fg_color="#0b0b0f")

        # Set up database

        setup_database()

        # Show login screen

        self.show_login()

    # Remove the current screen

    def clear(self):

        for current_widget in self.winfo_children():

            current_widget.destroy()

    # Show login screen

    def show_login(self):

        self.clear()

        LoginFrame(
            self,
            self.show_signup,
            self.show_chat
        ).pack(
            fill="both",
            expand=True
        )

    # Show signup screen

    def show_signup(self):

        self.clear()

        SignupFrame(
            self,
            self.show_chat,
            self.show_login
        ).pack(
            fill="both",
            expand=True
        )

    # Show chat screen

    def show_chat(self):

        self.clear()

        ChatFrame(
            self
        ).pack(
            fill="both",
            expand=True
        )

if __name__ == "__main__":
    App().mainloop()