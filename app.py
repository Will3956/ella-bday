import streamlit as st
from datetime import datetime
import json
import os
import requests

st.set_page_config(page_title="Happy Birthday Ella! 🎂", page_icon="🎉", layout="centered")

# --- Hidden Admin Login Button & Panel ---

# CSS for hidden login button top-left corner
st.markdown("""
<style>
#hidden-login {
    position: fixed;
    top: 5px;
    left: 5px;
    width: 40px;
    height: 40px;
    background: transparent;
    border: none;
    cursor: pointer;
    z-index: 10000;
}
#hidden-login:hover {
    background: rgba(255, 51, 153, 0.2);
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

if 'show_admin' not in st.session_state:
    st.session_state['show_admin'] = False
if 'admin_pw_input' not in st.session_state:
    st.session_state['admin_pw_input'] = ""

# Hidden login button triggers password input
if st.button(" ", key="hidden-login", help="Admin login (hidden)"):
    st.session_state['admin_pw_input'] = st.text_input("Enter admin password:", type="password")

# If password entered, check it
if st.session_state.get('admin_pw_input'):
    if st.session_state['admin_pw_input'] == "P1cklesC@t":
        st.session_state['show_admin'] = True
        st.success("🔓 Access granted!")
        st.session_state['admin_pw_input'] = ""  # reset input after success
    else:
        st.error("❌ Wrong password!")
        st.session_state['admin_pw_input'] = ""  # reset input on fail

# --- Messages storage ---

MESSAGES_FILE = "messages.json"

def load_messages():
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # If file is corrupt, start fresh
            return []
    return []

def save_messages(messages):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f)

def add_message(name, message):
    messages = load_messages()
    messages.append({"name": name, "message": message})
    save_messages(messages)

# --- CSS and layout for main app ---

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
    <p><em>With lots of love, <strong>Will</strong></em></p>
</div>
""", unsafe_allow_html=True)

# 🎶 Background birthday song
st.markdown("""
<audio autoplay>
  <source src="https://cdn.pixabay.com/download/audio/2023/03/19/audio_763c1e5705.mp3?filename=happy-birthday-instrumental-11603.mp3" type="audio/mpeg">
</audio>
""", unsafe_allow_html=True)

# --- Birthday messages form ---

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

# --- Show birthday messages live ---

st.markdown("### 🎂 Birthday Messages for Ella 🎂")

messages = load_messages()
for msg in reversed(messages):
    st.markdown(f"""
    <div class="message-box">
        <b>{msg['name']}</b><br>
        {msg['message']}
    </div>
    """, unsafe_allow_html=True)

# --- Auto-refresh messages every 5 seconds using Streamlit's experimental_rerun ---

import time

# Run this only if not in admin mode to avoid interrupting admin panel usage
if not st.session_state['show_admin']:
    time.sleep(5)
    st.experimental_rerun()

# --- Admin Panel (if logged in) ---

if st.session_state['show_admin']:
    st.markdown("---")
    st.markdown("## 🔐 Admin Panel")

    # Get visitor IP via public API
    try:
        ip = requests.get("https://api.ipify.org").text
        st.write(f"**Visitor IP:** {ip}")
    except Exception:
        st.error("Could not fetch IP address.")

    # Get IP geolocation from ipinfo.io
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json")
        geo = res.json()
        loc = geo.get("loc", "")
        city = geo.get("city", "Unknown city")
        region = geo.get("region", "Unknown region")
        country = geo.get("country", "Unknown country")
        st.write(f"**Location:** {city}, {region}, {country}")
        if loc:
            lat, lon = loc.split(",")
            # OpenStreetMap embed URL for small map
            map_url = f"https://www.openstreetmap.org/export/embed.html?bbox={float(lon)-0.05}%2C{float(lat)-0.05}%2C{float(lon)+0.05}%2C{float(lat)+0.05}&layer=mapnik&marker={lat}%2C{lon}"
            st.markdown(f'<iframe width="100%" height="300" src="{map_url}"></iframe>', unsafe_allow_html=True)
    except Exception:
        st.error("Could not fetch location data.")

    # Site preview iframe (replace URL with your actual site URL or GitHub Pages URL)
    st.markdown("### 🌐 Site Preview")
    st.markdown("""
    <iframe src="https://your-site-url-or-github-page" width="100%" height="400" style="border:1px solid #ff3399; border-radius:10px;"></iframe>
    """, unsafe_allow_html=True)
