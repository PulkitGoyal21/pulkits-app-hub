import streamlit as st
from collections import Counter, defaultdict

st.title("Wordle Solver by Pulkit Goyal")

# ---------- LOAD WORDS ----------
with open("wordle_answers.txt", "r") as f:
    WORDS_MASTER = [w.strip().lower() for w in f if len(w.strip()) == 5]

# ---------- INIT STATE ----------
def init_state():
    st.session_state.words = WORDS_MASTER.copy()
    st.session_state.min_count = defaultdict(int)
    st.session_state.max_count = defaultdict(lambda: 5)
    st.session_state.positional_bans = [set() for _ in range(5)]
    st.session_state.known_positions = [None] * 5
    st.session_state.guess = None
    st.session_state.solved = False
    st.session_state.feedback = ""

if "words" not in st.session_state:
    init_state()

# ---------- HELPERS ----------
def valid_word(word):
    wc = Counter(word)

    for ch, c in st.session_state.min_count.items():
        if wc[ch] < c:
            return False

    for ch, c in st.session_state.max_count.items():
        if wc[ch] > c:
            return False

    for i, ch in enumerate(word):
        if st.session_state.known_positions[i] and ch != st.session_state.known_positions[i]:
            return False
        if ch in st.session_state.positional_bans[i]:
            return False

    return True


def get_best_word(words):
    if not words:
        return None
    freq = Counter()
    for w in words:
        for ch in set(w):
            freq[ch] += 1
    return max(words, key=lambda w: sum(freq[ch] for ch in set(w)))


# ---------- MAIN ----------
if not st.session_state.solved:
    if st.session_state.guess is None:
        st.session_state.guess = get_best_word(st.session_state.words)

    if not st.session_state.guess:
        st.error("No words left. Inconsistent feedback.")
    else:
        st.markdown(f"### PROPOSED GUESS: **{st.session_state.guess.upper()}**")

        st.text_input(
            "ENTER FEEDBACK (G/Y/B)",
            key="feedback",
            max_chars=5
        )

        if st.button("Next"):
            fb = st.session_state.feedback.lower().strip()

            if fb == "ggggg":
                st.session_state.solved = True
                st.rerun()

            if len(fb) != 5 or any(c not in "gyb" for c in fb):
                st.error("Invalid feedback")
            else:
                guess = st.session_state.guess
                this_guess_mins = Counter()

                for i, status in enumerate(fb):
                    if status in ("g", "y"):
                        this_guess_mins[guess[i]] += 1

                for i, (status, ch) in enumerate(zip(fb, guess)):
                    if status == "g":
                        st.session_state.known_positions[i] = ch
                    elif status == "y":
                        st.session_state.positional_bans[i].add(ch)
                    elif status == "b":
                        st.session_state.positional_bans[i].add(ch)
                        st.session_state.max_count[ch] = this_guess_mins[ch]

                for ch, c in this_guess_mins.items():
                    st.session_state.min_count[ch] = max(
                        st.session_state.min_count[ch], c
                    )

                st.session_state.words = [
                    w for w in st.session_state.words
                    if valid_word(w) and w != guess
                ]

                st.session_state.guess = get_best_word(st.session_state.words)
                st.rerun()

else:
    st.success("Solved 🎉")

# ---------- RESTART ----------
if st.button("Restart"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()
