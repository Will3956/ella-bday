import streamlit as st
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="Happy Birthday Ella! 🎂", page_icon="🎉", layout="centered")

st.markdown("""
<style>
  /* Container for the pennant banner */
  .pennant-container {
    position: fixed;
    top: 10px;
    right: 150px;
    display: flex;
    gap: 4px;
    z-index: 9999;
    user-select: none;
  }

  /* Each small triangle flag */
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

  /* Birthday message with pink balloons - bigger font size */
  .birthday-header {
    text-align: center;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    font-size: 48px;  /* Increased font size */
    color: #ff3399;  
    margin: 80px auto 10px;
    user-select: none;
  }
  /* bigger pink balloons */
  .birthday-header .balloons {
    font-size: 60px; /* Bigger balloons too */
    vertical-align: middle;
  }

  /* Birthday message below */
  .birthday-text {
    text-align: center;
    font-family: 'Comic Sans MS', cursive, sans-serif;
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

# Image uploader
uploaded_image = st.file_uploader("Upload a special photo for Ella (optional)", type=["png", "jpg", "jpeg"])
if uploaded_image:
    img = Image.open(uploaded_image)
    st.image(img, caption="🎂 Ella's Special Moment", use_column_width=True)

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

# Birthday wish form
with st.form("wish_form"):
    wish = st.text_input("Write your birthday message to Ella 💌")
    submitted = st.form_submit_button("Send Wish")
    if submitted and wish.strip():
        st.success("🎉 Your wish has been sent!")
        st.write(f"💬 You said: *{wish}*")
