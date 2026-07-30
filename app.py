
import streamlit as st
import google.generativeai as genai
from PIL import Image

# १. पेजची सेटिंग
st.set_page_config(
    page_title="ShevgAI संवाद | Drumstick Expert",
    page_icon="🌿",
    layout="centered"
)

# २. UI डिझाईन
st.title("🌿 ShevgAI संवाद")
st.caption("आमची माती, आमची माणसं.")
st.write("रावसाहेब, इथे तुम्ही शेवगा बागेविषयी कोणतेही प्रश्न थेट विचारू शकता आणि हवे असल्यास फोटोही पाठवू शकता!")

# ३. API Key जोडणी
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("API Key सापडली नाही! कृपया Streamlit च्या Advanced Settings मध्ये Secrets तपासा.")
    st.stop()

# ४. ShevgAI चे तज्ञ मार्गदर्शन (System Prompt)
SYSTEM_PROMPT = """
तुम्ही एक प्रगत शेती तज्ञ (Agricultural Expert) आणि 'ShevgAI' आहात. 
विशेषतः शेवगा (Moringa/Drumstick) शेतीमध्ये तुमचा हातखंडा आहे. 
रावसाहेब यांच्या ५४० झाडांच्या बागेसाठी, रोग-कीड नियंत्रण, 00:52:34 व 00:45:45 खत व्यवस्थापन, पाणी व्यवस्थापन आणि आगामी छाटणी याबद्दल अत्यंत अचूक मार्गदर्शन करा. 
तुमची संपूर्ण उत्तरे फक्त आणि फक्त 'मराठी' भाषेत (Devanagari script) असली पाहिजेत आणि प्रत्येक उत्तरात आदराने 'रावसाहेब' असा उल्लेख करा.
"""

model = genai.GenerativeModel('', system_instruction=SYSTEM_PROMPT)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
# ५. चॅट हिस्टरी जपण्यासाठी सेशन स्टेट
if "messages" not in st.session_state:
    st.session_state.messages = []

# आधी झालेला संवाद स्क्रीनवर दाखवणे
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "image" in message and message["image"] is not None:
            st.image(message["image"], width=200)
        st.markdown(message["content"])

# ६. फोटो अपलोड करण्याची पर्यायी सोय (चॅटसोबत फोटो पाठवण्यासाठी)
uploaded_file = st.file_uploader("बागेचा फोटो अपलोड करा (पर्यायी - फोटोबद्दल प्रश्न विचारण्यासाठी)", type=["jpg", "jpeg", "png"])

# ७. वापरकर्त्यासाठी मेसेज टाईप करण्याचा बॉक्स (चॅट इनपुट)
if user_prompt := st.chat_input("शेवगा बागेविषयी तुमचा प्रश्न इथे विचार करा..."):
    
    current_image = None
    if uploaded_file is not None:
        current_image = Image.open(uploaded_file)
    
    # वापरकर्त्याचा मेसेज स्क्रीनवर दाखवणे
    with st.chat_message("user"):
        if current_image:
            st.image(current_image, width=200)
        st.markdown(user_prompt)
    
    # हिस्टरीमध्ये सेव्ह करणे
    st.session_state.messages.append({"role": "user", "content": user_prompt, "image": current_image})
    
    # ॲपचे उत्तर जनरेट करणे
    with st.chat_message("assistant"):
        with st.spinner("ShevgAI विचार करत आहे..."):
            try:
                contents = [user_prompt]
                if current_image:
                    contents.append(current_image)
                
                response = model.generate_content(contents)
                reply_text = response.text
                
                st.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text, "image": None})
            except Exception as e:
                st.error(f"तांत्रिक अडचण आली: {e}")
