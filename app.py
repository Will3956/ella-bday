import streamlit as st
import json
import os
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Happy Birthday Ella! 🎂", page_icon="🎉", layout="centered")

MESSAGES_FILE = "messages.json"
PASSWORD = "P1cklesC@t"

def load_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            try:
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

def get_ip_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return {}

def render_main_content():
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

def display_messages(container):
    messages = load_messages()
    with container:
        st.markdown("### 🎂 Birthday Messages for Ella 🎂")
        for msg in reversed(messages):
            st.markdown(f"""
            <div style="
                border: 2px solid #ff3399;
                border-radius: 10px;
                padding: 10px;
                margin: 10px auto;
                width: 70%;
                background-color: #ffe6f0;
                font-family: 'Comic Sans MS', cursive;
                color: #cc0066;
                ">
                <b>{msg['name']}</b><br>
                {msg['message']}
            </div>
            """)

# SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False

# Hidden login button top-left corner (invisible)
st.markdown("""
<style>
  #hidden-login {
    position: fixed;
    top: 0;
    left: 0;
    width: 35px;
    height: 35px;
    background: transparent;
    border: none;
    z-index: 99999;
    cursor: pointer;
  }
  #hidden-login:focus {
    outline: none;
  }
</style>
""", unsafe_allow_html=True)

login_clicked = st.button("", key="hidden-login")

if login_clicked:
    st.session_state.show_login = True

if st.session_state.show_login and not st.session_state.logged_in:
    pwd = st.text_input("Enter admin password:", type="password", key="pwd_input")
    if pwd:
        if pwd == PASSWORD:
            st.session_state.logged_in = True
            st.success("Welcome, Admin! 👑")
        else:
            st.error("Incorrect password!")

# Autorefresh interval (5 seconds)
interval = 5_000

if not st.session_state.logged_in:
    # Main site with message form and messages
    render_main_content()

    with st.form("wish_form"):
        name = st.text_input("Your Name", key="name_input")
        wish = st.text_input("Write your birthday message to Ella 💌", key="wish_input")
        submitted = st.form_submit_button("Send Wish")
        if submitted:
            if not name.strip() or not wish.strip():
                st.warning("Please enter both your name and your message!")
            else:
                add_message(name.strip(), wish.strip())
                st.success("🎉 Your wish has been sent!")

    message_refresher = st_autorefresh(interval=interval, limit=None, key="msg_refresh")

    messages_container = st.empty()
    display_messages(messages_container)

else:
    # Admin panel with modern styling
    st.markdown("""
    <style>
      body, .main {
        background-color: #1f2937;  /* Dark slate */
        color: #e0e7ff;  /* Light lavender */
      }
      .admin-header {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        color: #c7d2fe;
      }
      .card {
        background-color: #374151;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 25px;
      }
      .ip-info-title {
        font-weight: 600;
        font-size: 18px;
        margin-bottom: 10px;
        color: #a5b4fc;
      }
      .ban-btn {
        background-color: #ef4444;
        color: white;
        border: none;
        padding: 10px 18px;
        font-weight: 600;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-top: 10px;
      }
      .ban-btn:hover {
        background-color: #b91c1c;
      }
      .site-preview {
        background-color: #111827;
        border-radius: 12px;
        padding: 15px;
        box-shadow: inset 0 0 10px rgba(255,255,255,0.1);
        max-height: 600px;
        overflow-y: auto;
      }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="admin-header">Admin Panel - IP Tracking & Live Preview</div>')

    # Admin panel container
    with st.container():
        # IP info card
        ip = requests.get("https://api.ipify.org").text
        ip_info = get_ip_info(ip)

        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="ip-info-title">Your IP Information</div>', unsafe_allow_html=True)
            st.markdown(f"**IP Address:** {ip}")
            st.json(ip_info)

            if st.button("Ban this IP"):
                st.warning(f"IP {ip} banned! (placeholder, no backend)")

            st.markdown('</div>', unsafe_allow_html=True)

        # Live site preview card
        preview_refresher = st_autorefresh(interval=interval, limit=None, key="preview_refresh")
        with st.container():
            st.markdown('<div class="card site-preview">', unsafe_allow_html=True)
            st.markdown("### Live Site Preview")
            render_main_content()
            messages_preview = st.container()
            display_messages(messages_preview)
            st.markdown('</div>', unsafe_allow_html=True)
