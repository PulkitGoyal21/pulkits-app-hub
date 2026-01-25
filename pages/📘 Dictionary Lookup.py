import streamlit as st
import requests

st.set_page_config(page_title="Dictionary App", layout="centered")
st.title("📘 Dictionary App")

word = st.text_input("Enter a word")

if st.button("Search"):
    if not word.strip():
        st.warning("Enter a word first")
        st.stop()

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    with st.spinner("Looking up word..."):
        response = requests.get(url)

    if response.status_code == 200:
        data = response.json()[0]

        st.subheader(f"Word: {data['word']}")

        for meaning in data["meanings"]:
            st.markdown(f"### Part of Speech: `{meaning['partOfSpeech']}`")

            for d in meaning["definitions"]:
                st.write("• **Definition:**", d["definition"])
                if "example" in d:
                    st.caption(f"Example: {d['example']}")

            if meaning.get("synonyms"):
                st.write("**Synonyms:**", ", ".join(meaning["synonyms"]))

    else:
        st.error("Word not found!")
