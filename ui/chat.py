import customtkinter as ctk
import threading
from groq_ai import send_message_to_ai
from chat_storage import save_message, load_user_messages

class ChatFrame(ctk.CTkFrame):

    def __init__(self, parent_window, logout_callback, user_id):
        super().__init__(parent_window, fg_color="#0b0b0f")

        self.logout_callback = logout_callback
        self.user_id = user_id
        self.is_loading = False
        self.logout_button = None

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
        ).pack(side="right", padx=(0, 15))

        # Logout button
        self.logout_button = ctk.CTkButton(
            header_frame,
            text="Log out",
            width=80,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=13),
            fg_color="#2a2a35",
            hover_color="#3a3a45",
            command=self.logout
        )
        self.logout_button.pack(side="right", padx=15)

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

        # Load chat history
        self.load_chat_history()

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

    # Load chat history
    def load_chat_history(self):

        messages = load_user_messages(self.user_id)

        if messages:

            self.empty_message.pack_forget()

            for message_text, is_user_message in messages:

                self.add_message(message_text, is_user_message, False)

            # Scroll to bottom after loading all messages
            self.after(100, lambda: self.messages_frame._parent_canvas.yview_moveto(1))

    def send_message(self):
        if self.is_loading:
            return

        message_text = self.message_input.get().strip()

        if not message_text:
            return

        self.empty_message.pack_forget()
        self.add_message(message_text, True)
        self.message_input.delete(0, "end")

        # Save user message to database
        save_message(self.user_id, message_text, True)

        # Show loading state
        self.is_loading = True
        loading_message = self.add_message("Thinking...", False)

        # Start Groq request in background thread
        thread = threading.Thread(
            target=self.get_ai_response,
            args=(message_text, loading_message)
        )
        thread.daemon = True
        thread.start()

    def get_ai_response(self, user_message, loading_message):
        ai_response = send_message_to_ai(user_message)

        # Schedule the update on main thread with delay
        # Use after() to switch to main thread, then another after() for delay
        self.after(0, lambda: self.schedule_delayed_update(ai_response, loading_message))

    def schedule_delayed_update(self, ai_response, loading_message):
        # Add 1.5 second delay then show response
        self.after(1500, lambda: self.update_ai_response(ai_response, loading_message))

    def update_ai_response(self, ai_response, loading_message):
        self.is_loading = False

        # Remove loading message
        loading_message.destroy()

        if ai_response:
            self.add_message(ai_response, False)

            # Save AI response to database
            save_message(self.user_id, ai_response, False)
        else:
            self.add_message(
                "Unable to get a response. Please try again.",
                False
            )

    def logout(self):
        # Disable logout button
        self.logout_button.configure(state="disabled")

        # Hide empty message if visible
        if hasattr(self, 'empty_message'):
            self.empty_message.pack_forget()

        # Show logging out message
        logout_message = ctk.CTkLabel(
            self.messages_frame,
            text="Logging out...",
            text_color="#777783"
        )
        logout_message.pack(pady=10)

        # Wait 1.5 seconds then complete logout
        self.after(1500, lambda: self.complete_logout(logout_message))

    def complete_logout(self, logout_message):
        # Reset loading state
        self.is_loading = False

        # Re-enable logout button for next session
        self.logout_button.configure(state="normal")

        # Clear all messages
        for widget in self.messages_frame.winfo_children():
            widget.destroy()

        # Show empty state again
        self.empty_message = ctk.CTkLabel(
            self.messages_frame,
            text="✦\n\nHow can I help you today?",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#555560"
        )
        self.empty_message.pack(expand=True, pady=150)

        # Return to login
        self.logout_callback()

    def add_message(self, message_text, is_user, auto_scroll=True):
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

        if auto_scroll:
            self.after(
                50,
                lambda: self.messages_frame._parent_canvas.yview_moveto(1)
            )

        return message_frame