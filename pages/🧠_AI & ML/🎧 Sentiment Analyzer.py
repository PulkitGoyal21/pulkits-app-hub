import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sentiment Analyzer", layout="centered")

st.title("🎧 Boat Headphones Review Analyzer")
st.caption("ML model + human vibes + zero BS")

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    return joblib.load("sentiment_model.pkl")

model = load_model()
classes = list(model.classes_)

# ---------- INPUT ----------
review = st.text_area(
    "Enter a product review",
    height=120,
    placeholder="These headphones sound insane for the price..."
)

# ---------- PREDICT ----------
if st.button("Analyze 🔥"):
    if not review.strip():
        st.warning("Bro at least type something 💀")
        st.stop()

    with st.spinner("Analyzing sentiment..."):
        probs = model.predict_proba([review])[0]

    Ppos = probs[classes.index("pos")]
    Pneg = probs[classes.index("neg")]

    score = Ppos - Pneg
    normalised = (score + 1) / 2 * 100

    # ---------- COMMENT LOGIC (UNCHANGED) ----------
    if score <= -0.60:
        comment = "Extremely horrible review."
    elif score <= -0.30:
        comment = "Bad review."
    elif score <= -0.10:
        comment = "Somewhat negative review."
    elif score <= 0.10:
        comment = "Neutral review."
    elif score <= 0.30:
        comment = "Somewhat positive review."
    elif score <= 0.60:
        comment = "Good review."
    else:
        comment = "Amazing review."

    # ---------- OUTPUT ----------
    st.subheader("🧠 Verdict")
    st.success(comment)
    st.metric("Positivity", f"{round(normalised)} %")

    # ---------- PLOT (STREAMLIT-SAFE) ----------
    def plot_bar(score):
        fig, ax = plt.subplots(figsize=(10, 1.5))

        gradient = np.linspace(-1, 1, 1000).reshape(1, -1)
        cmap = plt.colormaps.get_cmap("RdYlGn")

        ax.imshow(
            gradient,
            aspect="auto",
            cmap=cmap,
            extent=(-1, 1, 0, 1)
        )

        ax.axvline(score, color="black", linewidth=3)

        ax.set_title(f"Sentiment Score: {score:.2f}", fontsize=12)
        ax.set_yticks([])
        ax.set_xticks([-1, -0.5, 0, 0.5, 1])
        ax.set_xlabel("← Negative     Neutral     Positive →")

        return fig

    st.subheader("📊 Sentiment Bar")
    st.pyplot(plot_bar(score))
