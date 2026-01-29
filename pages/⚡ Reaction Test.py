import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=100, key="reaction_refresh")

st.title("⚡ Reaction Test")
st.markdown("How fast can you press the button?")

st.divider()
st.subheader("Press the button as soon as it turns green.")

if not 'phase' in st.session_state:
    st.session_state.phase = 'idle'

if not 'start_time' in st.session_state:
    st.session_state.start_time = 0.0

if not 'click_time' in st.session_state:
    st.session_state.click_time = 0.0

if not 'go_time' in st.session_state:
    st.session_state.go_time = 0.0

if not 'reaction_time' in st.session_state:
    st.session_state.reaction_time = 0.0

if st.session_state.phase == 'idle':
    start_clicked = st.button("Start")

elif st.session_state.phase == 'waiting':
    st.info("Wait for green...")

elif st.session_state.phase == 'ready':
    st.success("CLICK NOW")
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        button_clicked = st.button("CLICK!", use_container_width=True)

elif st.session_state.phase == 'done':
    st.metric("Reaction Time (ms)", int(st.session_state.reaction_time * 1000))
    rt = st.session_state.reaction_time * 1000  # ms
    if rt < 300:
        verdict = "⚡ INSANE reflexes"
    elif rt < 380:
        verdict = "🔥 Very fast"
    elif rt < 450:
        verdict = "😎 Above average"
    elif rt < 550:
        verdict = "🙂 Average human"
    else:
        verdict = "💀 You blinked"
    
    st.markdown(verdict)

    restart_clicked = st.button("Try again")


if st.session_state.phase == "idle":
    if start_clicked:
        st.session_state.start_time = time.time()
        st.session_state.go_time = st.session_state.start_time + random.randint(2,5)
        st.session_state.phase = "waiting"

elif st.session_state.phase == "ready":
    if button_clicked:
        st.session_state.click_time = time.time()
        st.session_state.reaction_time = st.session_state.click_time - st.session_state.go_time -0.15
        st.session_state.phase = "done"

elif st.session_state.phase == "done":
    if restart_clicked:
        st.session_state.phase = "idle"

if st.session_state.phase == "waiting" and time.time() >= st.session_state.go_time:
    st.session_state.phase = "ready"

