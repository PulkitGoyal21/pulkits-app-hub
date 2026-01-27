import streamlit as st
#import pyttsx3 as tt
import speech_recognition as sr
import soundfile as sf
import time

st.title("🗣️🔊 Speech recognition and generation")
choice = st.radio("Choose to recognise or generate speech", ['🎙️ Recognise', '🔊 Generate'])


if choice == '🎙️ Recognise':
    with st.container(border=True):
        col1, gap, col2 = st.columns([1,0.15,1])

        r = sr.Recognizer()

        text = "—"
        audio_length = 0.0

        with col1:
            st.markdown("### 🗣️ Speech recognition")
            audio_file = st.audio_input("🎙️ Record voice")

        if audio_file:
            with st.spinner("Thinking..."):
                # Read audio safely
                data, samplerate = sf.read(audio_file)
                audio_length = round(len(data) / samplerate, 2)

                time.sleep(1.5)

                # Reset pointer (IMPORTANT)
                audio_file.seek(0)

                with sr.AudioFile(audio_file) as source:
                    audio = r.record(source)

                try:
                    text = r.recognize_google(audio)
                    st.toast("Speech recognized 🎧")
                except:
                    text = "Could not understand audio"

        with col2:
            st.markdown("### 🧠 Transcribed Text")
            st.markdown(
                f"""
                <div style="height:250px; overflow-y:auto;
                            padding:1rem; border:1px solid #444;
                            border-radius:10px;">
                {text}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col1:
            st.metric("Audio length", f"{audio_length}s")
            st.metric("Text length", len(text))

else:
    with st.container(border=True):
        st.markdown("### 🔊 Speech generation")

        #engine = tt.init()

        input_text = st.text_input("Enter text")

        if st.button("Speak 🔊"):
            #engine.say(input_text)
            with st.spinner("Preparing to speak..."):
                time.sleep(2.5)
            st.components.v1.html(f"""
            <script>
            const msg = new SpeechSynthesisUtterance("{input_text}");
            speechSynthesis.speak(msg);
            </script>
            """)                  
            #engine.runAndWait()
            st.toast("Speech generated 🎧")