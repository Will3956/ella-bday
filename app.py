import streamlit as st
from datetime import datetime
import json
import os
import requests

st.set_page_config(page_title="Happy Birthday Ella! 🎂", page_icon="🎉", layout="centered")

# File to save messages
MESSAGES_FILE = "messages.json"

# Load messages
def load_messages():
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
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

# Hidden login password
PASSWORD = "P1cklesC@t"

# CSS for the page + hidden login button top-left corner
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
  /* Hidden login button: completely invisible, no pointer change */
  #hidden-login {
    position: fixed;
    top: 0;
    left: 0;
    width: 30px;
    height: 30px;
    background: transparent;
    border: none;
    z-index: 10000;
    cursor: default;
    outline: none;
  }
  #hidden-login:hover {
    background: transparent !important;
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

<!-- Main Header -->
<div class="birthday-header">
  <span class="balloons">🎈</span>
  Happy Birthday Ella!
  <span class="balloons">🎈</span>
</div>

<div class="birthday-text">
    <p>Hi Ella! 🎉</p>
    <p>Wishing you an amazing birthday filled with love, laughter, and lots of delicious cake 🍰.</p>
    <p>May your day be as wonderful and bright as you are! 💖</p>
    <p><em>With lots of love, <strong>Charlie</strong></em></p>
</div>
""", unsafe_allow_html=True)

# 🎶 Background birthday song
st.markdown("""
<audio autoplay>
  <source src="https://cdn.pixabay.com/download/audio/2023/03/19/audio_763c1e5705.mp3?filename=happy-birthday-instrumental-11603.mp3" type="audio/mpeg">
</audio>
""", unsafe_allow_html=True)

# Hidden login button form
login_clicked = st.button("", key="hidden-login")

if login_clicked:
    password_input = st.text_input("Enter admin password:", type="password")
    if password_input == PASSWORD:
        st.success("Access granted! Here is the admin panel:")
        
        # Get visitor IP (may depend on hosting environment)
        try:
            ip_req = requests.get('https://api.ipify.org?format=json')
            ip = ip_req.json().get("ip", "Unknown IP")
        except Exception:
            ip = "Unable to fetch IP"
        st.write(f"Visitor IP: {ip}")
        
        # Try getting geolocation info
        try:
            geo_req = requests.get(f'https://ipapi.co/{ip}/json/')
            geo_data = geo_req.json()
            city = geo_data.get("city", "Unknown")
            region = geo_data.get("region", "Unknown")
            country = geo_data.get("country_name", "Unknown")
            st.write(f"Location: {city}, {region}, {country}")
        except Exception:
            st.write("Unable to fetch geolocation data.")
        
        # Show a preview of the site inside an iframe
        st.markdown("### Site Preview:")
        st.components.v1.iframe("https://your-site-url.com", height=500)  # Replace with actual deployed site URL
        
    elif password_input:
        st.error("Wrong password!")

# 💌 Birthday message form
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

# 🎂 Display birthday messages
st.markdown("### 🎂 Birthday Messages for Ella 🎂")

messages = load_messages()
for msg in reversed(messages):
    st.markdown(f"""
    <div class="message-box">
        <b>{msg['name']}</b><br>
        {msg['message']}
    </div>
    """, unsafe_allow_html=True)

# Auto-refresh every 5 seconds to update messages
st.experimental_rerun()
