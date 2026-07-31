import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
os.environ["GEMINI_API_KEY"] ="AQ.Ab8RN6JMsRRYJU9XEUntgigYcPkCePvatkB0S4UlIlnXgjprNw"
model = genai.GenerativeModel('gemini-1.5-flash')
st.set_page_config(page_title="ShevgAI संवाद", page_icon="🌿")
st.title("🌿 ShevgAI संवाद")
st.write("आमची माती, आमची माणसं.")
st.markdown("---")
uploaded_file = st.file_uploader("बागेचा किंवा पानाचा/खोडाचा फोटो अपलोड करा", type=['jpg', 'jpeg', 'png'])
user_prompt = st.text_input("शेवगा बागेविषयी तुमचा प्रश्न इथे टाईप करा...")
if st.button("माहिती मिळवा"):
    if uploaded_file or user_prompt:
        with st.spinner("माहिती शोधत आहे..."):
            try:
                inputs = []
                if uploaded_file:
                    inputs.append(Image.open(uploaded_file))
                if user_prompt:
                    inputs.append(user_prompt)
                else:
                    inputs.append("या शेवगा बागेच्या फोटोचे निरीक्षण करून छाटणी, रोग आणि कीड नियंत्रणाविषयी मार्गदर्शन करा.")
                
                response = model.generate_content(inputs)
                st.success("मार्गदर्शन:")
                st.write(response.text)
            except Exception as e:
                st.error(f"एरर आला आहे: {e}")
    else:
        st.warning("कृपया फोटो अपलोड करा किंवा प्रश्न लिहा.")
