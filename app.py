import streamlit as st
import json
import os
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Happy Birthday Ella! 🎂", page_icon="🎉", layout="centered")

MESSAGES_FILE = "messages.json"

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

# CSS + hidden login button as before
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
  }
  #hidden-login:focus {
    outline: none;
  }
</style>
""", unsafe_allow_html=True)

hidden_password = "P1cklesC@t"

if "login_clicked" not in st.session_state:
    st.session_state.login_clicked = False
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

clicked = st.button("", key="hidden-login")
if clicked:
    st.session_state.login_clicked = True

if st.session_state.login_clicked and not st.session_state.logged_in:
    pwd = st.text_input("Enter password to login:", type="password", key="pwd_input")
    if pwd:
        if pwd == hidden_password:
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Wrong password!")

# Banner and main page content (outside any container)
def render_main_content():
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

render_main_content()

# Message form
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

# Partial refresh of messages only - refresh every 10 seconds
count = st_autorefresh(interval=10_000, limit=None, key="message_autorefresh")

messages_container = st.empty()

def display_messages():
    messages = load_messages()
    with messages_container.container():
        st.markdown("### 🎂 Birthday Messages for Ella 🎂")
        for msg in reversed(messages):
            st.markdown(f"""
            <div class="message-box">
                <b>{msg['name']}</b><br>
                {msg['message']}
            </div>
            """, unsafe_allow_html=True)

display_messages()

# Admin panel preview (only if logged in)
if st.session_state.logged_in:
    st.markdown("---")
    st.markdown("## Admin Panel Preview (Live Site Content)")
    # Show exact current page content preview (reuse render_main_content)
    render_main_content()
