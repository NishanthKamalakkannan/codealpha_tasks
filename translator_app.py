import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os

# 🌟 Custom CSS for Updated Colors & Glassy Effects
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1519608487953-e999c86e7455');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .main-container {
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        background-color: rgba(17, 25, 40, 0.6);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0px 10px 40px rgba(0, 0, 0, 0.6);
        transition: transform 0.3s ease-in-out;
    }
    .main-container:hover {
        transform: scale(1.02);
    }
    h1 {
        color: #FFD700;
        font-family: 'Arial', sans-serif;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff7eb3 0%, #ff758c 100%);
        color: white;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        border-radius: 15px;
        border: none;
        box-shadow: 0px 5px 20px rgba(255, 117, 140, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%);
        transform: translateY(-4px);
        box-shadow: 0px 10px 25px rgba(255, 117, 140, 0.6);
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.3);
        color: #fff;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: box-shadow 0.3s ease;
    }
    .stTextInput>div>div>input:hover, .stTextArea>div>textarea:hover {
        box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.2);
    }
    .stSelectbox>div>div {
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.2);
        color: #fff;
        backdrop-filter: blur(5px);
    }
    .stDownloadButton>button {
        background: linear-gradient(135deg, #42e695 0%, #3bb2b8 100%);
        color: white;
        border-radius: 15px;
        padding: 0.5rem 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .stDownloadButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 10px 30px rgba(66, 230, 149, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# 🌍 Title and Description
st.markdown("""
    <div class="main-container">
        <h1>🌌 Lux Translator</h1>
        <p style="text-align: center; color: #e0e0e0; font-size: 18px;">💬 Translate, Listen & Download your text in a stunning interface.</p>
    </div>
""", unsafe_allow_html=True)

# 🌐 Dynamically Fetch Available Languages
lang_options = {name.title(): code for code, name in LANGUAGES.items()}

# 📝 Text Input Area
st.markdown('<div class="main-container">', unsafe_allow_html=True)
text_to_translate = st.text_area("📝 Enter Text:", height=190, placeholder="Type text here...")

# 📁 File Upload for Batch Translation
uploaded_file = st.file_uploader("📂 Or Upload a Text File (TXT only)", type=["txt"])
if uploaded_file is not None:
    text_to_translate = uploaded_file.read().decode("utf-8")
    st.success("✅ File uploaded successfully!")

# 🌐 Language Dropdown
target_language = st.selectbox("🌐 Choose target language:", list(lang_options.keys()))
target_language_code = lang_options[target_language]

# 🔄 Translation Logic
if st.button("🔄 Translate"):
    if text_to_translate and target_language_code:
        translator = Translator()
        try:
            # 🌟 Detect Source Language
            detected_lang = translator.detect(text_to_translate)
            detected_lang_name = LANGUAGES.get(detected_lang.lang, 'Unknown').title()
            st.info(f"🌟 *Detected Source Language:* {detected_lang_name}")

            # 🌐 Translate
            translated = translator.translate(text_to_translate, dest=target_language_code)
            st.success(f"✅ *Translated Text ({target_language}):*\n\n{translated.text}")

            # 💾 Download Translated Text
            st.download_button("📥 Download Translation", translated.text, file_name="translated.txt")

            # 🔊 Text-to-Speech
            tts = gTTS(translated.text, lang=target_language_code)
            tts.save("translated_audio.mp3")
            with open("translated_audio.mp3", "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")
            os.remove("translated_audio.mp3")

        except Exception as e:
            st.error(f"⚡ *An error occurred:* {str(e)}")
    else:
        st.warning("⚠ *Please enter text or upload a file, and select a target language.*")

st.markdown('</div>', unsafe_allow_html=True)

# 🎉 Footer
st.markdown("""
    <div class="main-container" style="text-align: center; margin-top: 20px;">
        <p style="color: #e0e0e0;">💡 <em>Built with ❤ using <strong>Streamlit</strong>, <strong>Googletrans</strong> & <strong>gTTS</strong> 🚀</em></p>
    </div>
""", unsafe_allow_html=True)
