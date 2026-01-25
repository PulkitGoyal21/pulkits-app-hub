import streamlit as st
import string
import joblib

st.title("💪 Password Strength Checker")
st.subheader("This program does not store your password")

password = st.text_input("Enter password", value="pass@123")

model_bundle = joblib.load("password_strength.pkl")
model = model_bundle["model"]
features = model_bundle["features"]

def strength(password):
    score = 1.0
    reasons = []

    # ---- Length (highest priority) ----
    length = len(password)
    if length < 8:
        score -= 0.5
        reasons.append("⚠️ Too short.")
    elif length < 10:
        score -= 0.3
        reasons.append("⚠️ Short length")
    elif length < 16:
        score -= 0.15
        reasons.append("✅ Decent length")
    else:
        score += 0.2   # reward long passwords
        reasons.append("💪 Long password")

    # ---- Character tracking ----
    char_dict = {}
    types = {'upper':0, 'lower':0, 'digit':0, 'symbol':0}

    max_repeat_run = 1
    current_run = 1

    for i, ch in enumerate(password):
        # count chars
        char_dict[ch] = char_dict.get(ch, 0) + 1

        # char types
        if ch.isupper(): types['upper'] += 1
        elif ch.islower(): types['lower'] += 1
        elif ch.isdigit(): types['digit'] += 1
        elif ch in string.punctuation: types['symbol'] += 1

        # consecutive repeats
        if i > 0 and ch == password[i-1]:
            current_run += 1
            max_repeat_run = max(max_repeat_run, current_run)
        else:
            current_run = 1

        # sequential pattern (abc / 123)
        if i >= 2:
            a, b, c = password[i-2], password[i-1], ch
            if ord(b) - ord(a) == 1 and ord(c) - ord(b) == 1:
                score -= 0.3
                reasons.append("⚠️ Sequential pattern detected (abc / 123)")
            if ord(a) - ord(b) == 1 and ord(b) - ord(c) == 1:
                score -= 0.3
                reasons.append("⚠️ Reverse sequence detected")

    # ---- Penalize long repeats ----
    if max_repeat_run >= 3:
        score -= 0.25
        reasons.append("⚠️ Repeated characters")

    # ---- Palindrome ----
    if password == password[::-1] and length > 3:
        score -= 0.2
        reasons.append("⚠️ Palindromes are easy to crack")

    # ---- Character variety ----
    for t in types:
        if types[t] == 0:
            score -= 0.15
            reasons.append(f"⚠️ Missing {t}")

    # ---- Use ML ----
    ml_input = [[
        int(types['lower'] > 0),
        int(types['upper'] > 0),
        int(types['symbol'] > 0),
        length
    ]]

    pred = model.predict(ml_input)[0]

    if pred == 2:
        score += 0.3
        reasons.append("🤖 ML model agrees it's strong")
    elif pred==1:
        reasons.append("🤖 ML model thinks its ok")
    elif pred == 0:
        score -= 0.15
        reasons.append("🤖 ML model flags weakness")

    # ---- Clamp score ----
    score = max(0.0, min(1.0, score))

    return round(score, 2), reasons

final_score,reasons = strength(password)
st.metric("Strength score", f"{int(final_score*100)}%")

if final_score < 0.3:
    st.error("Weak 💀")
elif final_score < 0.6:
    st.warning("Medium 😐")
else:
    st.success("Strong 💪")

st.subheader("Why?")
for r in reasons:
    st.write("•", r)