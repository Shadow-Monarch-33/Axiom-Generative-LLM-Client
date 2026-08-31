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

        self.title("Axiom")
        self.geometry("900x650")
        self.minsize(700, 550)
        self.configure(fg_color="#0b0b0f")

        # Current user
        self.current_user_id = None

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
            self.show_chat_with_user
        ).pack(
            fill="both",
            expand=True
        )

    # Show signup screen

    def show_signup(self):

        self.clear()

        SignupFrame(
            self,
            self.show_chat_with_user,
            self.show_login
        ).pack(
            fill="both",
            expand=True
        )

    # Show chat screen with user ID
    def show_chat_with_user(self, user_id):

        self.show_chat(user_id)

    # Show chat screen

    def show_chat(self, user_id):

        self.current_user_id = user_id

        self.clear()

        ChatFrame(
            self,
            self.handle_logout,
            self.current_user_id
        ).pack(
            fill="both",
            expand=True
        )

    # Handle logout
    def handle_logout(self):

        self.current_user_id = None
        self.show_login()

if __name__ == "__main__":
    App().mainloop()