# Axiom

Axiom is a small desktop AI assistant I built using Python.

The idea was pretty simple: I wanted to make a basic AI chat application with its own login system, database, and desktop interface instead of just making another chatbot website.

## What it does

- Create an account and log in
- Save accounts using MySQL
- Keep a separate chat for each account
- Remember previous messages after closing the app
- Chat with an AI using the Groq API
- Log out and switch accounts
- Simple dark desktop UI

Each account has its own chat, so if two different users log in, they won't see each other's messages.

## Built with

- Python
- CustomTkinter
- MySQL
- Groq API
- python-dotenv

## How it works

When a user sends a message, it gets saved to the database along with their user ID. The previous conversation is then loaded and sent to the AI as context.

The AI's response is also saved, so the conversation doesn't disappear when the application is closed.

The basic flow is:

```text
Login
  ↓
User account
  ↓
Chat
  ↓
MySQL + Groq
  ↓
AI response