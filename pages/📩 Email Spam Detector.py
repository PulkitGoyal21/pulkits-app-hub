import streamlit as st
import joblib
import numpy as np
from scipy.sparse import hstack, csr_matrix

# Load model + vectorizer
rfc = joblib.load("spam_rfc_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

spam_words = ['free', 'win', 'winner', 'urgent', 'click', 'offer',
              'buy now', 'limited', 'cash', 'prize', 'guaranteed']

spam_special_chars = ['$', '!', '#', '%', '@', '*', '^', '&', '_',
                      '-', '~', '?', '<', '>', '(', ')', '[', ']', '{', '}']

st.title("📧 Email Spam Detector")
st.write("Paste an email below to check if it’s spam.")

email_text = st.text_area("Email content")

if st.button("Detect Spam"):
    if email_text.strip() == "":
        st.warning("Enter some text first.")
    else:
        # TF-IDF features
        X_text = vectorizer.transform([email_text])

        # Extra handcrafted features
        X_other = np.array([
            email_text.count('!'),
            sum(1 for w in email_text.split() if w.isupper()),
            sum(word in email_text.lower().split() for word in spam_words),
            sum(email_text.count(c) for c in spam_special_chars),
            int('dear' in email_text.lower().split()),
            sum(c.isdigit() for c in email_text)
        ])

        X_other_sparse = csr_matrix(X_other.reshape(1, -1))
        X_combined = hstack([X_text, X_other_sparse])

        proba = rfc.predict_proba(X_combined)[0][1]  # spam probability

        threshold = 0.75  # tune this

        if proba >= threshold:
            st.error(f"🚨 This email is SPAM ({proba*100:.1f}% confidence)")
        else:
            st.success(f"✅ This email is NOT spam ({(1-proba)*100:.1f}% confidence)")

