import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

st.title("🔄 Random Spinner")
choices_text = st.text_area("Enter the choices (one per line)", value='Burger\nPizza\nBiryani')

choices = [c.strip() for c in choices_text.splitlines() if c.strip()]

if not choices:
    st.warning("Add at least one choice")
    st.stop()

if 'phase' not in st.session_state:
    st.session_state.phase = 'idle'

if 'ans' not in st.session_state:
    st.session_state.ans = None


if 'spin' not in st.session_state:
    st.session_state.spin = 0

if 'spin_end' not in st.session_state:
    st.session_state.spin_end = 0.0

if 'spin_start' not in st.session_state:
    st.session_state.spin_start = 0.0

PALETTE = [
    "#e74c3c",  # red
    "#3498db",  # blue
    "#2ecc71",  # green
    "#f1c40f",  # yellow
    "#9b59b6",  # purple
    "#e67e22",  # orange
]

if (
    'color_map' not in st.session_state
    or 'last_choices' not in st.session_state
    or st.session_state.last_choices != choices
):
    random.shuffle(PALETTE)
    st.session_state.color_map = {
        c: PALETTE[i % len(PALETTE)]
        for i, c in enumerate(choices)
    }
    st.session_state.last_choices = choices


if st.session_state.phase == 'idle':
    if st.button("Spin"):
        st.session_state.phase = 'spinning'
        st.session_state.spin_start = time.time()
        st.session_state.spin_end = st.session_state.spin_start + random.uniform(5.5, 10.5)

if st.session_state.phase == "spinning":
    now = time.time()
    progress = (now - st.session_state.spin_start) / (
        st.session_state.spin_end - st.session_state.spin_start
    )
    progress = min(progress, 1.0)

    st.session_state.spin = random.randint(0, len(choices)-1)
    current = choices[st.session_state.spin]
    color = st.session_state.color_map[current]

    st.markdown(
        f"""
        <h1 style="
            text-align:center;
            color:{color};
            font-size:60px;
            font-weight:800;
        ">
            {current}
        </h1>
        """,
        unsafe_allow_html=True
    )

    if time.time() >= st.session_state.spin_end:
        st.session_state.ans = choices[st.session_state.spin]
        st.session_state.phase = "done"
    if st.session_state.phase == "spinning":
        st_autorefresh(
            interval=int(50 + (progress**2) * 400),
            key="spin_refresh"
        )


if st.session_state.phase == 'done':
    st.markdown(f"### The winner is: {st.session_state.ans}")
    st.balloons()
    if st.button("Spin again"):
        st.session_state.phase = 'idle'
        st.rerun()