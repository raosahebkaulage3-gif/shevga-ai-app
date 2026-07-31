
import streamlit as st
import google.generativeai as genai
from PIL import Image

# १. इथे तुमची गुगल API Key टाका (उद्धरण चिन्हांमध्ये "")
GOOGLE_API_KEY = "TUMCHI_API_KEY_ITHE_TAKA" 

# API Key कन्फिगर करणे
genai.configure(api_key=GOOGLE_API_KEY)

# गुगलच्या अचूक मॉडेलची निवड
model = genai.GenerativeModel('gemini-1.5-flash')

# पेजचे सेटिंग
st.set_page_config(page_title="ShevgAI संवाद", page_icon="🌿")

# ॲपचे मुख्य टायटल आणि माहिती
st.title("🌿 ShevgAI संवाद")
st.write("आमची माती, आमची माणसं.")
st.write("रावसाहेब, शेवग्याच्या बागेच्या उत्तम व्यवस्थापनासाठी इथे प्रश्न विचारा किंवा फोटो अपलोड करा.")
st.markdown("---")

# --- इथून सुरू होतो आपला नवीन फॉर्म (कवच) ---
with st.form(key='shevga_form'):
    
    # फोटो घेण्यासाठी
    uploaded_file = st.file_uploader("बागेचा किंवा पानाचा/खोडाचा फोटो अपलोड करा (पर्यायी)", type=['jpg', 'jpeg', 'png'])
    
    # प्रश्न विचारण्यासाठी
    user_prompt = st.text_input("शेवगा बागेविषयी तुमचा प्रश्न इथे टाईप करा...")
    
    # माहिती पाठवण्याचे मुख्य बटन (हे दाबल्याशिवाय ॲप गुगलकडे जाणार नाही)
    submit_button = st.form_submit_button(label='माहिती मिळवा')

# जेव्हा तुम्ही 'माहिती मिळवा' बटन दाबाल, तेव्हाच पुढची प्रक्रिया होईल
if submit_button:
    if uploaded_file or user_prompt:
        with st.spinner("माहिती शोधत आहे, कृपया थोडा वेळ थांबा..."):
            try:
                # जर फोटो आणि प्रश्न दोन्ही असेल
                if uploaded_file and user_prompt:
                    image = Image.open(uploaded_file)
                    response = model.generate_content([user_prompt, image])
                
                # जर फक्त फोटो असेल (प्रश्न नसेल)
                elif uploaded_file:
                    image = Image.open(uploaded_file)
                    default_prompt = "या फोटोचे काळजीपूर्वक निरीक्षण करा आणि शेतीच्या आणि पीक व्यवस्थापनाच्या दृष्टिकोनातून सविस्तर माहिती सांगा."
                    response = model.generate_content([default_prompt, image])
                
                # जर फक्त प्रश्न असेल (फोटो नसेल)
                else:
                    response = model.generate_content(user_prompt)
                
                # आलेले उत्तर स्क्रीनवर दाखवण्यासाठी
                st.success("माहिती मिळाली!")
                st.write(response.text)
                
            except Exception as e:
                # जर काही तांत्रिक अडचण आली तर लाल रंगात मेसेज दिसेल
                st.error(f"काहीतरी तांत्रिक अडचण आली आहे. एरर: {e}")
    else:
        # जर फोटो किंवा प्रश्न काहीच दिले नसेल तर
        st.warning("कृपया माहिती मिळवण्यासाठी आधी फोटो अपलोड करा किंवा प्रश्न टाईप करा.")
