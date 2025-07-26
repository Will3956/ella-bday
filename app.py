import streamlit as st
from datetime import datetime
import json
import os
import requests

st.set_page_config(page_title="Happy Birthday Ella! 🎂", page_icon="🎉", layout="centered")

# File to save messages
MESSAGES_FILE = "messages.json"

# Load messages from file
def load_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Save messages to file
def save_messages(messages):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f)

# Add a new message
def add_message(name, message):
    messages = load_messages()
    messages.append({"name": name, "message": message})
    save_messages(messages)

# Get IP info (using ipinfo.io API)
def get_ip_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return {}

# CSS for the page and hidden login button
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
  /* Hidden login button */
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
    cursor: pointer;
    /* Remove any tooltip or hover text */
  }
  #hidden-login:focus {
    outline: none;
  }
</style>
""", unsafe_allow_html=True)

# Hidden login button (completely invisible, no tooltip)
hidden_password = "P1cklesC@t"

# Render the hidden button
clicked = st.button(" ", key="hidden-login", help=None)

# Trick to add the ID and attributes to the button element to prevent tooltip:
st.markdown("""
<script>
const btn = window.parent.document.querySelector('button[kind="primary"][data-testid="stButton"][id^="hidden-login"]');
if (btn) {
  btn.id = 'hidden-login';
  btn.title = '';
  btn.setAttribute('aria-label', '');
</script>
""", unsafe_allow_html=True)

if clicked:
    pwd = st.text_input("Enter password to login:", type="password")
    if pwd == hidden_password:
        st.success("Login successful!")
        # Show IP info & preview here (simplified example)
        ip = st.text_input("Enter IP to lookup (or leave empty for your IP):").strip()
        if not ip:
            try:
                ip = requests.get("https://api.ipify.org").text
            except:
                ip = "Unknown"
        ip_info = get_ip_info(ip)
        st.write(f"IP Info for {ip}:")
        st.json(ip_info)
        # Preview message box for the site (simplified)
        st.markdown("<h3>Site Preview</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style='border: 2px solid #ff3399; border-radius:10px; padding:10px; background:#ffe6f0; color:#cc0066; font-family: Comic Sans MS, cursive; width: 70%; margin: 10px auto;'>
            <b>Charlie</b><br>
            🎉 Happy 16th Birthday, Ella! 🎂✈️<br>
            Wishing you an amazing day filled with love, laughter, and adventure! You’ve already seen so much of the world—can’t wait to see where you go next. Keep shining and exploring, globe-trotter! 🌍<br>
            <em>Lots of love, Charlie</em>
        </div>
        """, unsafe_allow_html=True)
    elif pwd:
        st.error("Wrong password!")

# Banner
st.markdown("""
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

# Birthday message form and display
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

st.markdown("### 🎂 Birthday Messages for Ella 🎂")
messages = load_messages()
for msg in reversed(messages):
    st.markdown(f"""
    <div class="message-box">
        <b>{msg['name']}</b><br>
        {msg['message']}
    </div>
    """, unsafe_allow_html=True)

# Auto refresh messages every 10 seconds (partial refresh)
st.markdown('<meta http-equiv="refresh" content="10">', unsafe_allow_html=True)
