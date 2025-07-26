import streamlit as st
import json
import os
import time
from datetime import datetime

st.set_page_config(page_title="Happy Birthday Ella! 🎂", page_icon="🎉", layout="centered")

MESSAGES_FILE = "messages.json"

# Functions for message handling
def load_messages():
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_messages(messages):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f)

def add_message(name, message):
    messages = load_messages()
    messages.append({"name": name, "message": message})
    save_messages(messages)

# Custom CSS for styling and hidden login
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
    font-family: 'Comic Sans MS', cursive;
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
    font-family: 'Comic Sans MS', cursive;
    font-size: 56px;
    color: #ff3399;
    margin: 100px auto 20px;
    user-select: none;
  }
  .birthday-header .balloons {
    font-size: 60px;
    vertical-align: middle;
  }
  .birthday-text {
    text-align: center;
    font-family: 'Comic Sans MS', cursive;
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
    font-family: 'Comic Sans MS', cursive;
    color: #cc0066;
  }
  #hidden-login {
    position: fixed;
    top: 0;
    left: 0;
    width: 30px;
    height: 30px;
    background: transparent;
    border: none;
    outline: none;
    box-shadow: none;
    appearance: none;
    z-index: 10000;
    cursor: default;
    user-select: none;
  }
  #hidden-login:hover {
    background: transparent !important;
  }
  #hidden-login:focus {
    outline: none;
    box-shadow: none;
  }
</style>

<!-- Banner -->
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

<!-- Hidden login button -->
<button id="hidden-login"></button>

<!-- Header -->
<div class="birthday-header">
  <span class="balloons">🎈</span>
  Happy Birthday Ella!
  <span class="balloons">🎈</span>
</div>

<!-- Messages from Will and Charlie -->
<div class="birthday-text">
  <p>Hi Ella! 🎉</p>
  <p>Wishing you an amazing birthday filled with love, laughter, and lots of delicious cake 🍰.</p>
  <p>May your day be as wonderful and bright as you are! 💖</p>
  <p><em>With lots of love, <strong>Will</strong></em></p>
  <br>
  <p>🎉 Happy 16th Birthday, Ella! 🎂️✈️</p>
  <p>Wishing you an amazing day filled with love, laughter, and adventure! You’ve already seen so much of the world—can’t wait to see where you go next. Keep shining and exploring, globe-trotter! 🌍</p>
  <p><em>Lots of love, <strong>Charlie</strong></em></p>
</div>

<!-- Music -->
<audio autoplay>
  <source src="https://cdn.pixabay.com/download/audio/2023/03/19/audio_763c1e5705.mp3?filename=happy-birthday-instrumental-11603.mp3" type="audio/mpeg">
</audio>
""", unsafe_allow_html=True)

# Message form
with st.form("wish_form"):
    name = st.text_input("Your Name")
    wish = st.text_input("Write your birthday message to Ella 💌")
    if st.form_submit_button("Send Wish"):
        if name.strip() and wish.strip():
            add_message(name.strip(), wish.strip())
            st.success("🎉 Your wish has been sent!")
        else:
            st.warning("Please fill out both fields.")

# Real-time message updates
message_container = st.empty()

for _ in range(300):  # Loop with ~5 minutes max
    messages = load_messages()
    with message_container.container():
        st.markdown("### 🎂 Birthday Messages for Ella 🎂")
        for msg in reversed(messages):
            st.markdown(f"""
            <div class='message-box'>
                <b>{msg['name']}</b><br>
                {msg['message']}
            </div>
            """, unsafe_allow_html=True)
    time.sleep(1)
