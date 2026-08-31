import customtkinter as ctk

from authentication import create_user, user_exists


class SignupFrame(ctk.CTkFrame):

    def __init__(self, parent_window, chat_callback, login_callback):

        super().__init__(parent_window, fg_color="#0b0b0f")

        self.chat_callback = chat_callback

        self.login_callback = login_callback

        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)

# Signup card

        self.signup_card_frame = ctk.CTkFrame(
            self,
            width=390,
            height=550,
            corner_radius=24,
            fg_color="#121218"
        )

        self.signup_card_frame.grid(row=0, column=0)

        self.signup_card_frame.grid_propagate(False)

# Logo

        ctk.CTkLabel(

            self.signup_card_frame,
            text="✦",
            font=ctk.CTkFont(size=34),
            text_color="#5b8cff"
        ).pack(pady=(38, 4))

# Title

        ctk.CTkLabel(
            self.signup_card_frame,
            text="Create your account",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack()

# Subtitle

        ctk.CTkLabel(
            self.signup_card_frame,
            text="Start chatting with Axiom",
            text_color="#777783"
        ).pack(pady=(5, 28))

# Name input

        self.name_input = ctk.CTkEntry(
            self.signup_card_frame, width=300, height=46,
            corner_radius=12,
            placeholder_text="Name"
        )

        self.name_input.pack(pady=6)

# Email input

        self.email_input = ctk.CTkEntry(
            self.signup_card_frame, 
            width=300, 
            height=46,
            corner_radius=12,
            placeholder_text="Email"
        )

        self.email_input.pack(pady=6)

# Password input

        self.password_input = ctk.CTkEntry(
            self.signup_card_frame, 
            width=300, 
            height=46,
            corner_radius=12,
            placeholder_text="Password",
            show="•"
        )

        self.password_input.pack(pady=6)

        # Confirm password input

        self.confirm_password_input = ctk.CTkEntry(
            self.signup_card_frame, 
            width=300, 
            height=46,
            corner_radius=12,
            placeholder_text="Confirm password",
            show="•"
        )

        self.confirm_password_input.pack(pady=6)

        # Error message

        self.signup_error_message = ctk.CTkLabel(
            self.signup_card_frame,
            text="",
            text_color="#ff6b6b"
        )

        self.signup_error_message.pack(pady=5)

        # Signup button

        ctk.CTkButton(
            self.signup_card_frame,
            text="Create account",
            width=300,
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.signup
        ).pack(pady=(7, 15))

        # Login button

        ctk.CTkButton(
            self.signup_card_frame,
            text="Already have an account?  Log in",
            width=250,
            fg_color="transparent",
            hover_color="#1c1c26",
            text_color="#6f9aff",
            command=self.login_callback
        ).pack()

    # Signup

    def signup(self):

        name = self.name_input.get().strip()

        email = self.email_input.get().strip()

        password = self.password_input.get()

        confirm_password = self.confirm_password_input.get()

        if not all([
            name,
            email,
            password,
            confirm_password
        ]):

            self.signup_error_message.configure(
                text="Please fill in all fields."
            )

            return

        if password != confirm_password:

            self.signup_error_message.configure(
                text="Passwords do not match."
            )

            return

        if user_exists(email):

            self.signup_error_message.configure(
                text="An account with this email already exists."
            )

            return

        user_id = create_user(name, email, password)

        if not user_id:

            self.signup_error_message.configure(
                text="An account with this email already exists."
            )

            return

        self.signup_loading_message = ctk.CTkLabel(
            self.signup_card_frame,
            text="Creating your account...",
            text_color="#777783"
        )

        self.signup_loading_message.pack(pady=5)

        # Waits 2 secs before opening chat
        self.after(2000, lambda: self.chat_callback(user_id))