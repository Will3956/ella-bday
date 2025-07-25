import streamlit as st
from datetime import datetime
import json
import os

st.set_page_config(page_title="Happy Birthday Ella! 🎂", page_icon="🎉", layout="centered")

# File to save messages
MESSAGES_FILE = "messages.json"

# Load messages
def load_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            return json.load(f)
    return []

# Save messages
def save_messages(messages):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f)

# Add new message
def add_message(name, message):
    messages = load_messages()
    messages.append({"name": name, "message": message})
    save_messages(messages)

# Reveal target date
target = datetime(2026, 5, 5, 0, 0, 0)
now = datetime.now()

# CSS style for message box
st.markdown("""
<style>
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
  .countdown-container {
    display: flex;
    justify-content: center;
    gap: 80px;
    font-family: 'Comic Sans MS', cursive;
    color: #ff3399;
    margin-top: 150px;
    user-select: none;
  }
  .countdown-item {
    text-align: center;
  }
  .countdown-number {
    font-size: 80px;
    font-weight: bold;
  }
  .countdown-label {
    font-size: 36px;
  }
</style>
""", unsafe_allow_html=True)

if now < target:
    # Before May 5, 2026 - show spaced countdown and info
    delta = target - now
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    st.markdown(f"""
    <div style="text-align:center; font-family: 'Comic Sans MS', cursive; font-size: 48px; color: #ff3399; user-select:none;">
        ⏳ Countdown to Reveal ⏳
    </div>

    <div class="countdown-container">
      <div class="countdown-item">
        <div class="countdown-number">{days}</div>
        <div class="countdown-label">Days</div>
      </div>
      <div class="countdown-item">
        <div class="countdown-number">{hours:02d}</div>
        <div class="countdown-label">Hours</div>
      </div>
      <div class="countdown-item">
        <div class="countdown-number">{minutes:02d}</div>
        <div class="countdown-label">Minutes</div>
      </div>
      <div class="countdown-item">
        <div class="countdown-number">{seconds:02d}</div>
        <div class="countdown-label">Seconds</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("🎁 Messages and birthday greeting will be revealed on May 5, 2026! Stay tuned!")

else:
    # On or after May 5, 2026 - show full birthday greeting & wishes

    # Pennant banner and header + message
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
        font-family: 'Comic Sans MS', cursive;
        font-size: 22px;
        color: #ff3399;
        margin: 0 auto 30px;
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

    # Birthday song autoplay
    st.markdown("""
    <audio autoplay>
      <source src="https://cdn.pixabay.com/download/audio/2023/03/19/audio_763c1e5705.mp3?filename=happy-birthday-instrumental-11603.mp3" type="audio/mpeg">
    </audio>
    """, unsafe_allow_html=True)

    # Birthday message form
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

    # Display saved messages
    st.markdown("### 🎂 Birthday Wishes for Ella 🎂")
    messages = load_messages()
    for msg in reversed(messages):
        st.markdown(f"""
        <div class="message-box">
            <b>{msg['name']}</b><br>
            {msg['message']}
        </div>
        """, unsafe_allow_html=True)

# Auto-refresh every 15 seconds
st.markdown('<meta http-equiv="refresh" content="15">', unsafe_allow_html=True)
