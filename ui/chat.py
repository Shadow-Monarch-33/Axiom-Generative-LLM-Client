import customtkinter as ctk

class ChatFrame(ctk.CTkFrame):

    def __init__(self, parent_window):
        super().__init__(parent_window, fg_color="#0b0b0f")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        header_frame = ctk.CTkFrame(
            self,
            height=65,
            fg_color="#101016",
            corner_radius=0
        )
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)

        ctk.CTkLabel(
            header_frame,
            text="✦  AURA",
            font=ctk.CTkFont(size=19, weight="bold")
        ).pack(side="left", padx=28)

        ctk.CTkLabel(
            header_frame,
            text="●  Online",
            text_color="#72d68a",
            font=ctk.CTkFont(size=12)
        ).pack(side="right", padx=28)

        # Messages
        self.messages_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#0b0b0f",
            corner_radius=0
        )
        self.messages_frame.grid(
            row=1, column=0,
            sticky="nsew",
            padx=80, pady=25
        )

        # Empty state
        self.empty_message = ctk.CTkLabel(
            self.messages_frame,
            text="✦\n\nHow can I help you today?",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#555560"
        )
        self.empty_message.pack(expand=True, pady=150)

        # Input area
        input_frame = ctk.CTkFrame(
            self,
            fg_color="#0b0b0f"
        )
        input_frame.grid(
            row=2, column=0,
            sticky="ew",
            padx=80, pady=(0, 25)
        )
        input_frame.grid_columnconfigure(0, weight=1)

        self.message_input = ctk.CTkEntry(
            input_frame,
            height=52,
            corner_radius=16,
            border_width=1,
            border_color="#292932",
            fg_color="#14141b",
            placeholder_text="Ask anything..."
        )
        self.message_input.grid(
            row=0, column=0,
            sticky="ew",
            padx=(0, 10)
        )
        self.message_input.bind(
            "<Return>",
            lambda _: self.send_message()
        )

        ctk.CTkButton(
            input_frame,
            text="↑",
            width=52,
            height=52,
            corner_radius=16,
            font=ctk.CTkFont(size=20),
            command=self.send_message
        ).grid(row=0, column=1)

    def send_message(self):
        message_text = self.message_input.get().strip()

        if not message_text:
            return

        self.empty_message.pack_forget()
        self.add_message(message_text, True)
        self.message_input.delete(0, "end")

        # Temporary response
        self.add_message(
            "AI response will appear here once Groq is connected.",
            False
        )

    def add_message(self, message_text, is_user):
        message_frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color="#191921" if is_user else "#111117",
            corner_radius=14
        )
        message_frame.pack(
            fill="x",
            pady=6,
            padx=(100 if is_user else 0, 0 if is_user else 100)
        )

        ctk.CTkLabel(
            message_frame,
            text=message_text,
            justify="left",
            anchor="w",
            wraplength=600,
            font=ctk.CTkFont(size=14)
        ).pack(
            fill="x",
            padx=18,
            pady=14
        )

        self.after(
            50,
            lambda: self.messages_frame._parent_canvas.yview_moveto(1)
        )