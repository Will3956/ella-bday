import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="Happy Birthday Ella! 🎂", page_icon="🎉", layout="centered")

MESSAGES_FILE = "messages.json"
hidden_password = "P1cklesC@t"

def load_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            try:
                return json.load(f)
            except:
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

# CSS (same as before but added a container for admin and preview)
st.markdown("""
<style>
  /* birthday styling & hidden login omitted for brevity */
  .admin-panel {
    background-color: #1e293b;
    color: #f8fafc;
    padding: 20px;
    border-radius: 12px;
    margin: 30px auto 50px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    max-width: 900px;
  }
  .ip-info-title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 12px;
  }
  iframe {
    border-radius: 12px;
  }
  .ban-btn {
    background-color: #ef4444;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    margin-top: 15px;
  }
  .ban-btn:hover {
    background-color: #dc2626;
  }
  .site-preview {
    margin-top: 40px;
    background: white;
    border-radius: 12px;
    padding: 15px;
    max-width: 900px;
    color: #333;
    font-family: 'Comic Sans MS', cursive;
  }
</style>
""", unsafe_allow_html=True)

clicked = st.button(" ", key="hidden-login", help=None)

st.markdown("""
<script>
const btn = window.parent.document.querySelector('button[kind="primary"][data-testid="stButton"][id^="hidden-login"]');
if (btn) {
  btn.id = 'hidden-login';
  btn.title = '';
  btn.setAttribute('aria-label', '');
}
</script>
""", unsafe_allow_html=True)

if clicked:
    pwd = st.text_input("Enter password to login:", type="password")
    if pwd == hidden_password:
        st.success("Login successful!")

        # Autorefresh every 5 seconds (3000ms here to avoid flicker)
        count = st.experimental_singleton.get("refresh_count") if "refresh_count" in st.experimental_singleton else 0
        count = (count + 1) % 100000
        st.experimental_singleton.set("refresh_count", count)
        # Better to use st_autorefresh
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=5000, limit=None, key="autorefresh")

        # IP input & lookup
        ip = st.text_input("Enter IP to lookup (or leave empty for your IP):").strip()
        if not ip:
            try:
                ip = requests.get("https://api.ipify.org").text
            except:
                ip = "Unknown"

        ip_info = get_ip_info(ip)

        admin_panel = st.container()
        with admin_panel:
            st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
            st.markdown(f'<div class="ip-info-title">IP Information for: {ip}</div>')

            filtered_info = {k: v for k, v in ip_info.items() if k not in ("loc", "readme")}
            st.json(filtered_info)

            loc_str = ip_info.get("loc")
            if loc_str:
                lat, lon = map(float, loc_str.split(","))
                st.markdown("### IP Location Map (Google Maps)")
                google_maps_url = f"https://maps.google.com/maps?q={lat},{lon}&hl=en&z=14&output=embed"
                iframe_html = f"""
                <iframe 
                    width="100%" 
                    height="400" 
                    frameborder="0" 
                    style="border:0;" 
                    src="{google_maps_url}" 
                    allowfullscreen="" 
                    aria-hidden="false" 
                    tabindex="0">
                </iframe>
                """
                st.markdown(iframe_html, unsafe_allow_html=True)
            else:
                st.info("No location data available for this IP.")

            if st.button("Ban this IP"):
                st.warning(f"IP {ip} banned! (placeholder - implement your ban logic here)")
            st.markdown('</div>', unsafe_allow_html=True)

        # Live preview of birthday page below admin panel:
        preview = st.container()
        with preview:
            st.markdown('<div class="site-preview">', unsafe_allow_html=True)
            st.markdown("""
                <h1 style="color:#ff3399; font-family: 'Comic Sans MS', cursive;">🎈 Happy Birthday Ella! 🎈</h1>
                <p style="font-family: 'Comic Sans MS', cursive; font-size:18px; color:#cc0066;">
                    🎉 Happy 16th Birthday, Ella! 🎂✈️<br>
                    Wishing you an amazing day filled with love, laughter, and adventure! You’ve already seen so much of the world — can’t wait to see where you go next. Keep shining and exploring, globe-trotter! 🌍<br>
                    <em>Lots of love, Charlie</em>
                </p>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif pwd:
        st.error("Wrong password!")

# Birthday page UI below admin login area (same as before)

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

# Optional: refresh birthday messages every 10 sec (can comment out if you want no refresh)
st.markdown('<meta http-equiv="refresh" content="10">', unsafe_allow_html=True)
