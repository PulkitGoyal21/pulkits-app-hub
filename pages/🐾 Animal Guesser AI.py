import streamlit as st
import joblib

dtc = joblib.load("animal_dtc_model.pkl")

columns = [
    "hair", "feathers", "eggs", "milk", "airborne",
    "aquatic", "predator", "teeth", "backbone", "breath",
    "venomous", "fins", "legs", "tail", "domestic", "catsize", "class_type"
]

tree = dtc.tree_

st.title("🐾 Animal Guesser AI")
st.write("Answer the questions and I’ll guess the animal.")

# ---- session state init ----
if "node" not in st.session_state:
    st.session_state.node = 0
    st.session_state.finished = False

def reset():
    st.session_state.node = 0
    st.session_state.finished = False

# ---- traversal ----
if not st.session_state.finished:
    node = st.session_state.node

    if tree.feature[node] != -2:
        feature_index = tree.feature[node]
        threshold = tree.threshold[node]
        feature_name = columns[feature_index]

        # Special cases
        if feature_name == "legs":
            value = st.selectbox(
                "How many legs does the animal have?",
                [0, 2, 4, 6, 8]
            )
        elif feature_name == "class_type":
            value = st.selectbox(
                "What class is the animal?",
                [1, 2, 3, 4, 5, 6, 7],
                format_func=lambda x: [
                    "Mammal", "Bird", "Reptile",
                    "Fish", "Amphibian", "Insect", "Invertebrate"
                ][x-1]
            )
        else:
            value = st.radio(
                f"Does the animal have `{feature_name}`?",
                ["Yes", "No"],
                key=f"radio_{node}"
            )

            value = 1 if value == "Yes" else 0

        if st.button("Next"):
            if value <= threshold:
                st.session_state.node = tree.children_left[node]
            else:
                st.session_state.node = tree.children_right[node]

            st.rerun()

    else:
        predicted = dtc.classes_[tree.value[node].argmax()]
        st.success(f"🧠 I think the animal is: **{predicted}**")
        st.session_state.finished = True
        st.button("Restart", on_click=reset)
