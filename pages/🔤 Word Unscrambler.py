#Unscrambler
import streamlit as st

st.title("Word unscrambler")

with open("words.txt", 'r') as f:
    lst = f.read().splitlines()


word = st.text_input("Enter the scrambled word: ").lower()

matches = []

if word:
    for i in lst:
        if len(i) == len(word) and sorted(word) == sorted(i.lower()):
            matches.append(i.lower())

    if matches:
        st.success("Success!")
        for w in matches:
            st.markdown(f"- **{w}**")
    else:
        st.error("No matches found :(")
