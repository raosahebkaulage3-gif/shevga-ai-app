
import streamlit as st
import google.generativeai as genai
from PIL import Image

# गुगलची नवीन AQ चावी इथे थेट टाका
genai.configure(api_key="AQ.Ab8RN6JMsRRYJU9XEUntgigYPkCePvatkB0S4UlIIn...")

model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="ShevgAI संवाद", page_icon="🌿")

st.title("🌿 ShevgAI संवाद")
st.write("आमची माती, आमची माणसं.")
st.write("रावसाहेब, शेवगा बागेच्या उत्तम व्यवस्थापनासाठी इथे प्रश्न विचारा किंवा फोटो अपलोड करा.")
st.markdown("---")

uploaded_file = st.file_uploader("बागेचा किंवा पानाकडून/खोडाचा फोटो अपलोड करा (पर्यायी)", type=['jpg', 'jpeg', 'png'])
user_prompt = st.text_input("शेवगा बागेविषयी तुमचा प्रश्न इथे टाईप करा...")

if st.button("माहिती मिळवा"):
    if uploaded_file or user_prompt:
        with st.spinner("माहिती शोधत आहे, कृपया थोडा वेळ थांबा..."):
            try:
                inputs = []
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    inputs.append(image)
                if user_prompt:
                    inputs.append(user_prompt)
                else:
                    inputs.append("या शेवगा बागेच्या फोटोचे निरीक्षण करून छाटणी, रोग, कीड, पाणी आणि फळ धरण्याविषयी सविस्तर मार्गदर्शन करा.")
                
                response = model.generate_content(inputs)
                st.success("### शेवगा बागेविषयी मार्गदर्शन:")
                st.write(response.text)
            except Exception as e:
                st.error(f"काहीतरी तांत्रिक अडचण आली आहे. एरर: {e}")
    else:
                st.warning("कृपया फोटो अपलोड करा किंवा प्रश्न लिहा.")
