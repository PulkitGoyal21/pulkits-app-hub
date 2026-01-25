import random
from collections import defaultdict
import matplotlib.pyplot as plt
import streamlit as st

# --- Game setup ---
moves = ["R", "P", "S"]
decay = 0.9

# --- Session state init ---
if "transitions" not in st.session_state:
    st.session_state.transitions = defaultdict(lambda: defaultdict(int))
    st.session_state.wins = []
    st.session_state.prev = None
    st.session_state.started = False

def update_wins(player, ai):
    if player == ai:
        st.session_state.wins.append(0)
    elif (player == "R" and ai == "S") or \
         (player == "P" and ai == "R") or \
         (player == "S" and ai == "P"):
        st.session_state.wins.append(1)
    else:
        st.session_state.wins.append(-1)

def ai_move(prev, current):
    for m in moves:
        st.session_state.transitions[prev][m] *= decay
    st.session_state.transitions[prev][current] += 1

    total = sum(st.session_state.transitions[prev].values())
    probs = [st.session_state.transitions[prev][m] / total for m in moves]

    predicted = random.choices(moves, probs)[0]
    return {"R": "P", "P": "S", "S": "R"}[predicted]

# --- UI ---
st.title("🧠 Rock Paper Scissors AI")

st.write("Click a move. AI adapts over time.")

cols = st.columns(3)

for i, move in enumerate(moves):
    if cols[i].button(move):
        if not st.session_state.started:
            ai = random.choice(moves)
            st.session_state.started = True
        else:
            ai = ai_move(st.session_state.prev, move)

        update_wins(move, ai)
        st.session_state.prev = move

        st.success(f"AI played: **{ai}**")

# --- Plot ---
if st.session_state.wins:
    labels = ["Win", "Draw", "Loss"]
    sizes = [
        st.session_state.wins.count(1),
        st.session_state.wins.count(0),
        st.session_state.wins.count(-1)
    ]

    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        explode=(0.1, 0, 0),
        colors=["green", "grey", "red"]
    )
    ax.set_title("Wins / Draws / Losses")
    ax.axis("equal")

    st.pyplot(fig)
