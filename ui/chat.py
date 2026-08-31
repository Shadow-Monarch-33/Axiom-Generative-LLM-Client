import customtkinter as ctk
import threading
from groq_ai import Assistant
from chat_storage import save_message, load_user_messages, load_conversation_history

class ChatFrame(ctk.CTkFrame):

    def __init__(self, parent_window, logout_callback, user_id):
        super().__init__(parent_window, fg_color="#0a0a0e")

        self.logout_callback = logout_callback
        self.user_id = user_id
        self.is_loading = False

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        header_frame = ctk.CTkFrame(
            self,
            height=56,
            fg_color="#121218",
            corner_radius=0
        )
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)

        # Axiom branding
        ctk.CTkLabel(
            header_frame,
            text="Axiom",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#5b8cff"
        ).pack(side="left", padx=24)

        # Status indicator
        status_frame = ctk.CTkFrame(
            header_frame,
            fg_color="transparent"
        )
        status_frame.pack(side="left", padx=12)

        ctk.CTkLabel(
            status_frame,
            text="●",
            text_color="#72d68a",
            font=ctk.CTkFont(size=10)
        ).pack(side="left")

        ctk.CTkLabel(
            status_frame,
            text="Online",
            text_color="#777783",
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=(4, 0))

        # Logout button
        self.logout_button = ctk.CTkButton(
            header_frame,
            text="Log out",
            width=75,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color="#2a2a35",
            hover_color="#3a3a45",
            command=self.logout
        )
        self.logout_button.pack(side="right", padx=12)

        # Messages
        self.messages_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#0a0a0e",
            corner_radius=0
        )
        self.messages_frame.grid(
            row=1, column=0,
            sticky="nsew",
            padx=0,
            pady=0
        )

        # Empty state
        self.empty_message = ctk.CTkLabel(
            self.messages_frame,
            text="Axiom\n\nHow can I help you today?",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#555560"
        )
        self.empty_message.pack(expand=True, pady=180)

        # Load chat history
        self.load_chat_history()

        # Input area
        input_frame = ctk.CTkFrame(
            self,
            fg_color="#121218",
            height=80
        )
        input_frame.grid(
            row=2, column=0,
            sticky="ew"
        )
        input_frame.grid_columnconfigure(0, weight=1)

        # Input container
        input_container = ctk.CTkFrame(
            input_frame,
            fg_color="transparent"
        )
        input_container.pack(
            fill="x",
            expand=True,
            padx=20,
            pady=16
        )
        input_container.grid_columnconfigure(0, weight=1)

        self.message_input = ctk.CTkEntry(
            input_container,
            height=48,
            corner_radius=12,
            border_width=2,
            border_color="#292932",
            fg_color="#1a1a22",
            placeholder_text="Type your message...",
            placeholder_text_color="#555560"
        )
        self.message_input.grid(
            row=0, column=0,
            sticky="ew",
            padx=(0, 12)
        )
        self.message_input.bind(
            "<Return>",
            lambda _: self.send_message()
        )

        # Send button
        self.send_button = ctk.CTkButton(
            input_container,
            text="→",
            width=48,
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=18),
            fg_color="#4a7ab8",
            hover_color="#5b8aff",
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1)

        # AI client
        self.assistant = Assistant()

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
        self.send_button.configure(state="disabled")
        loading_message = self.add_message("Thinking...", False)

        # Start Groq request in background thread
        thread = threading.Thread(
            target=self.get_ai_response,
            args=(loading_message,)
        )
        thread.daemon = True
        thread.start()

    def get_ai_response(self, loading_message):
        # Load conversation history
        history = load_conversation_history(self.user_id)

        # Get AI response with history
        ai_response = self.assistant.generate_response(history)

        # Schedule the update on main thread with delay
        self.after(0, lambda: self.schedule_delayed_update(ai_response, loading_message))

    def schedule_delayed_update(self, ai_response, loading_message):
        # Add 1.5 second delay then show response
        self.after(1500, lambda: self.update_ai_response(ai_response, loading_message))

    def update_ai_response(self, ai_response, loading_message):
        self.is_loading = False
        self.send_button.configure(state="normal")

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
            text_color="#777783",
            font=ctk.CTkFont(size=14)
        )
        logout_message.pack(pady=12)

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
            text="Axiom\n\nHow can I help you today?",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#555560"
        )
        self.empty_message.pack(expand=True, pady=180)

        # Return to login
        self.logout_callback()

    def add_message(self, message_text, is_user, auto_scroll=True):
        # Message bubble colors
        bubble_color = "#243b73" if is_user else "#49305f"

        # Message row for alignment
        message_row = ctk.CTkFrame(
            self.messages_frame,
            fg_color="transparent"
        )
        message_row.pack(
            fill="x",
            pady=8
        )

        # Message bubble with self-sizing
        message_bubble = ctk.CTkFrame(
            message_row,
            fg_color=bubble_color,
            corner_radius=16
        )

        # Align user right, AI left
        if is_user:
            message_bubble.pack(side="right", padx=20)
        else:
            message_bubble.pack(side="left", padx=20)

        # Message label with max width
        message_label = ctk.CTkLabel(
            message_bubble,
            text=message_text,
            justify="left",
            anchor="w",
            wraplength=550,
            font=ctk.CTkFont(size=14),
            text_color="#e0e0e0"
        )
        message_label.pack(
            fill="x",
            padx=18,
            pady=14
        )

        if auto_scroll:
            self.after(
                50,
                lambda: self.messages_frame._parent_canvas.yview_moveto(1)
            )

        return message_row