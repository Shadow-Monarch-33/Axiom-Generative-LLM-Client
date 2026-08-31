import customtkinter as ctk

from authentication import login_user


class LoginFrame(ctk.CTkFrame):

    def __init__(self, parent_window, signup_callback, login_callback):

        super().__init__(parent_window, fg_color="#0b0b0f")

        self.signup_callback = signup_callback
        self.login_callback = login_callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Login card
        login_card_frame = ctk.CTkFrame(
            self,
            width=390,
            height=500,
            corner_radius=24,
            fg_color="#121218"
        )

        login_card_frame.grid(row=0, column=0)

        login_card_frame.grid_propagate(False)

        # Logo
        ctk.CTkLabel(
            login_card_frame,
            text="✦",
            font=ctk.CTkFont(size=34),
            text_color="#5b8cff"
        ).pack(pady=(55, 4))

        # Title
        ctk.CTkLabel(
            login_card_frame,
            text="Welcome back",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack()

        # Subtitle
        ctk.CTkLabel(
            login_card_frame,
            text="Sign in to continue to AURA",
            text_color="#777783",
            font=ctk.CTkFont(size=13)
        ).pack(pady=(5, 35))

        # Email input
        self.email_input = ctk.CTkEntry(
            login_card_frame,
            width=300,
            height=48,
            corner_radius=12,
            placeholder_text="Email"
        )

        self.email_input.pack(pady=7)

        # Password input
        self.password_input = ctk.CTkEntry(
            login_card_frame,
            width=300,
            height=48,
            corner_radius=12,
            placeholder_text="Password",
            show="•"
        )

        self.password_input.pack(pady=7)

        # Error message
        self.login_error_message = ctk.CTkLabel(
            login_card_frame,
            text="",
            text_color="#ff6b6b",
            font=ctk.CTkFont(size=12)
        )

        self.login_error_message.pack(pady=(5, 0))

        # Login button
        ctk.CTkButton(
            login_card_frame,
            text="Log in",
            width=300,
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.login
        ).pack(pady=(10, 18))

        # Sign up prompt
        ctk.CTkLabel(
            login_card_frame,
            text="Don't have an account?",
            text_color="#777783"
        ).pack(side="left", padx=(45, 4), pady=10)

        # Sign up button
        ctk.CTkButton(
            login_card_frame,
            text="Sign up",
            width=65,
            fg_color="transparent",
            hover_color="#1c1c26",
            text_color="#6f9aff",
            command=self.signup_callback
        ).pack(side="left")

    # Login
    def login(self):

        email_address = self.email_input.get().strip()
        password_text = self.password_input.get()

        if not email_address or not password_text:

            self.login_error_message.configure(
                text="Please enter your email and password."
            )

            return

        user_id = login_user(email_address, password_text)

        if not user_id:

            self.login_error_message.configure(
                text="Invalid email or password."
            )

            return

        self.login_callback(user_id)