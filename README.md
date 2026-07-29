import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="ShevgAI संवाद | Drumstick Expert",
    page_icon="🌿",
    layout="centered"
)

# UI Layout
st.title("🌿 ShevgAI संवाद")
st.caption("आमची माती, आमची माणसं.")
st.write("रावसाहेब, तुमच्या शेवगा (Drumstick) बागेतील झाडाचा किंवा पानाचा फोटो अपलोड करा आणि तात्काळ अचूक निदान व उपाय मिळवा.")

# API Setup (Streamlit Secrets मधून)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("API Key जोडलेली नाही. कृपया Streamlit Secrets तपासा.")

# Image Uploader
uploaded_file = st.file_uploader("शेवग्याच्या पानाचा किंवा झाडाचा फोटो निवडा...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="अपलोड केलेला फोटो", use_column_width=True)
    
    if st.button("निदान करा"):
        with st.spinner("फोटो तपासत आहे... कृपया प्रतीक्षा करा..."):
            try:
                # Gemini Vision Model
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # System Prompt / Instructions
                prompt = """
                तुम्ही एक तज्ज्ञ शेवगा (Drumstick/Moringa) शेती मार्गदर्शक आहात. 
                शेतकऱ्याने दिलेल्या फोटोचे बारकाईने निरीक्षण करा आणि खालील माहिती अचूक मराठीत द्या:
                १. रोग, कीड किंवा बुरशी (असल्यास)
                २. सध्याची वाढीची अवस्था (उदा. फुलांचा किंवा शेंगांचा टप्पा)
                ३. पाणी आणि खत व्यवस्थापन (उदा. 00:52:34 किंवा 00:45:45 चा योग्य वापर आणि गरज)
                ४. योग्य उपाय किंवा फवारणी
                नेहमी सकारात्मक आणि सोप्या भाषेत शेतकऱ्याला मार्गदर्शन करा.
                """
                
                response = model.generate_content([prompt, image])
                st.subheader("तज्ज्ञांचा सल्ला:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"काहीतरी तांत्रिक अडचण आली: {e}")

st.markdown("---")
st.caption("Developed for Smart Drumstick Farming | ShevgAI v1.0")
