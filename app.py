import streamlit as st
from datetime import datetime
from PIL import Image
import json
import os

st.set_page_config(page_title="Happy Birthday Ella! 🎂", page_icon="🎉", layout="centered")

# File to save messages
MESSAGES_FILE = "messages.json"

# Load messages from file or create empty list
def load_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            return json.load(f)
    else:
        return []

# Save messages to file
def save_messages(messages):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f)

# Add a new message to storage
def add_message(name, message):
    messages = load_messages()
    messages.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "message": message
    })
    save_messages(messages)

# --- UI code below ---

st.markdown("""
<style>
  .pennant-container {
    position: fixed;
    top: 10px;
    right: 150px;
    display: flex;
    gap: 4px;
    z-index: 9999;
    user-select: none;
  }
  .triangle-flag {
    width: 30px;
    height: 30px;
    background: linear-gradient(135deg, #ff3399, #cc0066);
    clip-path: polygon(0 0, 100% 0, 50% 100%);
    color: white;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    font-weight: bold;
    font-size: 18px;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: 5px;
    box-shadow: 0 0 6px rgba(255, 51, 153, 0.8);
  }
  .birthday-header {
    text-align: center;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    font-size: 48px;
    color: #ff3399;
    margin: 80px auto 10px;
    user-select: none;
  }
  .birthday-header .balloons {
    font-size: 60px;
    vertical-align: middle;
  }
  .birthday-text {
    text-align: center;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    font-size: 22px;
    color: #ff3399;
    margin: 0 auto 30px;
  }
  .message-box {
    border: 2px solid #ff3399;
    border-radius: 10px;
    padding: 10px;
    margin: 10px auto;
    width: 70%;
    background-color: #ffe6f0;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    color: #cc0066;
  }
</style>

<div class="pennant-container">
  <div class="triangle-flag">H</div>
  <div class="triangle-flag">A</div>
  <div class="triangle-flag">P</div>
  <div class="triangle-flag">P</div>
  <div class="triangle-flag">Y</div>
  <div class="triangle-flag">B</div>
  <div class="triangle-flag">I</div>
  <div class="triangle-flag">R</div>
  <div class="triangle-flag">T</div>
  <div class="triangle-flag">H</div>
  <div class="triangle-flag">D</div>
  <div class="triangle-flag">A</div>
  <div class="triangle-flag">Y</div>
</div>

<div class="birthday-header">
  <span class="balloons">🎈</span>
  Happy Birthday Ella!
  <span class="balloons">🎈</span>
</div>

<div class="birthday-text">
    <p>Hi Ella! 🎉</p>
    <p>Wishing you an amazing birthday filled with love, laughter, and lots of delicious cake 🍰.</p>
    <p>May your day be as wonderful and bright as you are! 💖</p>
    <p><em>With lots of love, <strong>Will</strong></em></p>
</div>
""", unsafe_allow_html=True)

# Birthday countdown
birthday_date = datetime(2025, 7, 25)
days_left = (birthday_date.date() - datetime.now().date()).days
if days_left > 0:
    st.success(f"🎁 Only {days_left} days left until Ella’s big day!")
elif days_left == 0:
    st.balloons()
    st.markdown("### 🎊 It's Ella’s Birthday Today! Happy Birthday! 🎊")
else:
    st.info("The birthday has passed, but every day is special with Ella! 💫")

# Autoplay instrumental birthday song (~30 seconds)
st.markdown("""
<audio autoplay>
  <source src="https://cdn.pixabay.com/download/audio/2023/03/19/audio_763c1e5705.mp3?filename=happy-birthday-instrumental-11603.mp3" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>
""", unsafe_allow_html=True)

# Birthday wish form with name input
with st.form("wish_form"):
    name = st.text_input("Your Name")
    wish = st.text_input("Write your birthday message to Ella 💌")
    submitted = st.form_submit_button("Send Wish")
    if submitted:
        if not name.strip() or not wish.strip():
            st.warning("Please enter both your name and your message!")
        else:
            add_message(name.strip(), wish.strip())
            st.success("🎉 Your wish has been sent!")

# Show all messages live, newest first with updated heading
st.markdown("### 🎂 Birthday Msg for Ella 🎂")

messages = load_messages()
for msg in reversed(messages):
    st.markdown(f"""
    <div class="message-box">
        <b>{msg['name']}</b> <i>on {msg['timestamp']}</i><br>
        {msg['message']}
    </div>
    """, unsafe_allow_html=True)
