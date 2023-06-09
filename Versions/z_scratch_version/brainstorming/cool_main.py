import openai
import os
from dotenv import load_dotenv
import tkinter as tk
import time

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create a Tkinter window
root = tk.Tk()
root.title("Nova System")
root.geometry("600x400")
root.configure(bg="black")

# Create a Tkinter label for displaying the AI response
response_label = tk.Label(root, fg="cyan", bg="black", font=("Courier", 12), wraplength=580)
response_label.pack(pady=20, padx=10)

def stream_to_console(message):
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.035)
    print()  # newline at the end

def stream_to_label(message, index=0):
    # Add one character to the label text and schedule the next character
    if index < len(message):
        response_label["text"] += message[index]
        root.after(35, stream_to_label, message, index + 1)

def stream_ai_response(user_input):
    # Call to the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    # Prepare response message
    response_message = f"AI's response: {response['choices'][0]['message']['content']}"

    # Stream to console
    stream_to_console(response_message)

    # Clear the previous response and stream the new response to the label
    response_label["text"] = ""
    stream_to_label(response_message)

def run_stream():
    user_input = user_input_entry.get()
    stream_ai_response(user_input)

# Create a Tkinter entry field and a submit button
user_input_entry = tk.Entry(root, font=("Courier", 12))
user_input_entry.pack(pady=20)

submit_button = tk.Button(root, text="Submit", command=run_stream, fg="white", bg="cyan", font=("Courier", 12))
submit_button.pack()

root.mainloop()
