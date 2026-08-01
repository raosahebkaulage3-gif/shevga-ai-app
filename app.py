
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Streamlit Secrets मधून सुरक्षितपणे चावी घेणे
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("कृपया Streamlit Secrets मध्ये GEMINI_API_KEY सेट करा.")

# मॉडेल आणि मराठी भाषेची सक्ती
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="You are an expert agricultural assistant for drumstick (shevga) farming. You must always reply strictly in Marathi language (मराठी भाषेतच उत्तरे द्या)."
)

# मोबाईल ॲपसारखा लूक देण्यासाठी पेज कॉन्फिगरेशन
st.set_page_config(page_title="ShevgAI - शेवगा सल्लागार", page_icon="🌿", layout="centered")

# कस्टम सीएसएस (CSS) द्वारे ॲपला मोबाईल ॲपसारखा मॉडर्न लूक देणे
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #2e7d32;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌿 ShevgAI - शेवगा कृषी सल्लागार")
st.write("आमची माती, आमची माणसं. तुमच्या शेवगा बागेचे अचूक डिजिटल डॉक्टर!")
st.markdown("---")

# युजर्ससाठी इनपुट क्षेत्र
uploaded_file = st.file_uploader("📸 बागेचा, पानाचा किंवा खोडाचा फोटो अपलोड करा", type=['jpg', 'jpeg', 'png'])
user_prompt = st.text_input("💬 शेवगा बागेविषयी तुमचा प्रश्न इथे टाईप करा...", placeholder="उदा. झाडाची पाने पिवळी पडत आहेत, काय करावे?")

if st.button("🔍 मार्गदर्शन मिळवा"):
    if uploaded_file or user_prompt:
        with st.spinner("🤖 कृषी सल्लागार माहिती शोधत आहे... कृपया प्रतीक्षा करा..."):
            try:
                inputs = []
                if uploaded_file:
                    inputs.append(Image.open(uploaded_file))
                if user_prompt:
                    inputs.append(user_prompt)
                else:
                    inputs.append("या शेवगा बागेच्या फोटोचे निरीक्षण करून छाटणी, रोग, कीड आणि फळधारणा याविषयी मराठीत सविस्तर मार्गदर्शन करा.")
                
                response = model.generate_content(inputs)
                st.markdown("### 📋 तज्ज्ञांचे मार्गदर्शन (मराठीत):")
                st.success(response.text)
            except Exception as e:
                st.error(f"तांत्रिक एरर आला आहे: {e}")
    else:
        st.warning("⚠️ कृपया आधी बागेचा फोटो अपलोड करा किंवा तुमचा प्रश्न लिहा.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2026 ShevgAI | ५० लाख शेतकऱ्यांच्या सेवेसाठी सज्ज</p>", unsafe_allow_html=True)
