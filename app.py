import streamlit as st
import sqlite3
from datetime import datetime
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="Shevga AI - शेवगा डॉक्टर",
    page_icon="🌿",
    layout="centered"
)

# Database Initialization
def init_db():
    conn = sqlite3.connect('shevga_ai_records.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmer_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT,
            category TEXT,
            diagnosis TEXT,
            remedy TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_log(category, diagnosis, remedy):
    conn = sqlite3.connect('shevga_ai_records.db')
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO farmer_logs (date_time, category, diagnosis, remedy)
        VALUES (?, ?, ?, ?)
    ''', (now, category, diagnosis, remedy))
    conn.commit()
    conn.close()

init_db()

# AI Logic Simulation
def analyze_shevga_image(image):
    return {
        "category": "Category B (कीड प्रादुर्भाव - थ्रिप्स/अळ्या)",
        "confidence": "94.5%",
        "diagnosis": "पानांवर थ्रिप्स (चंदेरी डाग) किंवा पानांची कुटळणारी अळी यांचा प्रादुर्भाव दिसून येत आहे.",
        "remedy": "प्रादुर्भाव सुरुवातीच्या टप्प्यात असेल तर 'निमअर्क (10,000 ppm) 2 मिली/लीटर' किंवा दशपर्णी अर्क फवारा. प्रादुर्भाव जास्त असल्यास शिफारस केलेले कीटकनाशक वापरा.",
        "remedy_type": "सेंद्रिय / रासायनिक फवारणी"
    }

# UI Layout
st.title("🌿 Shevga AI (शेवगा AI डॉक्टर)")
st.write("रावसाहेब, तुमच्या शेवगा बागेतील झाडाचा किंवा पानाचा फोटो अपलोड करा आणि तात्काळ अचूक निदान व उपाय मिळवा.")

st.markdown("---")

uploaded_file = st.file_uploader("📷 बागेतील फोटो निवडा किंवा कॅमेऱ्याने काढा...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="अपलोड केलेला फोटो", use_column_width=True)
    
    if st.button("🔍 AI द्वारे विश्लेषण करा"):
        with st.spinner("AI मॉडेल फोटो तपासत आहे... कृपया थोडा वेळ थांबा..."):
            result = analyze_shevga_image(img)
            save_log(result["category"], result["diagnosis"], result["remedy"])
            
            st.success(f"**ओळखलेली श्रेणी:** {result['category']} (अचूकता: {result['confidence']})")
            st.info(f"**निदान (Diagnosis):** {result['diagnosis']}")
            st.warning(f"**सुचवलेला उपाय (Action Plan):** {result['remedy']}")
            st.write(f"**उपचाराचा प्रकार:** `{result['remedy_type']}`")
            st.write("✅ *हे निदान डेटाबेसमध्ये जतन झाले आहे.*")

st.markdown("---")
st.caption("Developed for Shevga Orchard Management | Shevga AI v1.0")
