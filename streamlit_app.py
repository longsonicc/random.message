import streamlit as st
import re
import random
from datetime import datetime

st.title("Random Message Generator")

# Upload chat file
uploaded_file = st.file_uploader("Lade den Chatverlauf hoch(.txt)", type="txt")

# Function to parse chat messages
def parse_whatsapp_chat(text):
    messages = []
    pattern = re.compile(r'^(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}) - (.*?): (.*)$')
    current_message = None
    for line in text.splitlines():
        match = pattern.match(line)
        if match:
            date_str, time_str, sender, message = match.groups()
            timestamp = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
            if current_message:
                messages.append(current_message)
            current_message = {
                "timestamp": timestamp,
                "sender": sender,
                "message": message
            }
        else:
            if current_message:
                current_message["message"] += "\n" + line
    if current_message:
        messages.append(current_message)
    return messages

# After file is uploaded
if uploaded_file:
    chat_text = uploaded_file.read().decode("utf-8")
    messages = parse_whatsapp_chat(chat_text)
    senders = sorted(set(msg["sender"] for msg in messages))

    st.success(f"Loaded {len(messages)} messages from {len(senders)} participants.")

    # Menu options
    st.header("Was kann ich für dich tun?")
    choice = st.radio(["Zufällige Nachricht eines bestimmten Mitglieds", "Zufällige Nachricht mit einem bestimmten Wort"])

    if choice == "Zufällige Nachricht eines bestimmten Mitglieds":
        selected_sender = st.selectbox("Wähle ein Mitglied", senders)
        sender_messages = [msg["message"] for msg in messages if msg["sender"] == selected_sender]
        if sender_messages:
            if st.button("Show random message"):
                st.info(random.choice(sender_messages))
        else:
            st.warning("Diese Person hat noch nie eine Nachricht in der Gruppe verfasst.")

    elif choice == "Zufällige Nachricht mit einem bestimmten Wort":
        search_word = st.text_input("Wähle ein Wort").strip().lower()
        if search_word:
            matching_messages = [
                msg["message"] for msg in messages
                if search_word in msg["message"].lower()
            ]
            if matching_messages:
                if st.button("Show random message"):
                    st.info(random.choice(matching_messages))
            else:
                st.warning("Dieses Wort wurde noch nie im Chat benutzt.")
