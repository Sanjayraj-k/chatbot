import streamlit as st
from transformers import pipeline
import datetime

# Initialize Chatbot model for simple responses
chatbot = pipeline("text-generation", model="gpt2")  # Using a small model for quick responses

# Page configuration
st.set_page_config(page_title="Chennai Museum Ticket Booking Chatbot")

# Title and Introduction
st.title("Chennai Museum Ticket Booking Chatbot")
st.write("Welcome to the Chennai Museum! I can help you book tickets. Let’s get started!")

# Function to generate chatbot response
def generate_response(user_input):
    # Define basic responses for common questions
    if "ticket" in user_input.lower() or "book" in user_input.lower():
        return "Please tell me the number of tickets, date, and time you'd like to visit."
    elif "price" in user_input.lower() or "cost" in user_input.lower():
        return "The ticket costs ₹50 for adults and ₹20 for children."
    elif "hours" in user_input.lower():
        return "The museum is open from 9:00 AM to 5:00 PM, Tuesday to Sunday."
    else:
        # Fallback to language model for responses
        response = chatbot(user_input, max_length=50, num_return_sequences=1)
        return response[0]["generated_text"]

# Chat history storage
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# User input and interaction
user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        # Generate bot response
        bot_response = generate_response(user_input)
        
        # Add to chat history
        st.session_state["chat_history"].append({"user": user_input, "bot": bot_response})

# Display chat history
for chat in st.session_state["chat_history"]:
    st.write(f"You: {chat['user']}")
    st.write(f"Bot: {chat['bot']}")

# Ticket booking section
st.subheader("Ticket Booking Details")

# Booking form
with st.form("booking_form"):
    name = st.text_input("Name")
    num_tickets = st.number_input("Number of Tickets", min_value=1, step=1)
    date = st.date_input("Date of Visit", min_value=datetime.date.today())
    time = st.time_input("Time of Visit", value=datetime.time(10, 0))

    # Submit button
    submit_button = st.form_submit_button("Book Tickets")

# Confirmation message
if submit_button:
    if name and num_tickets > 0:
        st.success(f"Thank you, {name}! Your booking for {num_tickets} ticket(s) on {date} at {time} is confirmed.")
    else:
        st.error("Please fill in all details to complete your booking.")
