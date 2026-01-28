import streamlit as st
import numpy as np
import cv2

st.title("Face recognition and blurring")
st.markdown("This app does not store your pictures.")

img_file = st.camera_input("🙂 Click a picture")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

if img_file:
    bytes_data = img_file.getvalue()
    np_img = np.frombuffer(bytes_data, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    h, w = img.shape[:2]
    if w > 800:
        scale = 800 / w
        img = cv2.resize(img, (int(w*scale), int(h*scale)))


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=4,
        minSize=(60, 60)
    )


    if face_cascade.empty():
        st.error("Face cascade failed to load 😬")
    if len(faces)==0:
        st.warning("No face detected 😬")
    else:
        st.success(f"Detected a face(s)! 🙂")
        img_boxed = img.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(
                img_boxed,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),  # green box
                2             # thickness
            )

        st.image(
            cv2.cvtColor(img_boxed, cv2.COLOR_BGR2RGB),
            caption="Detected Face(s)"
        )

    
        mode = st.radio(
            "Blur mode",
            ["Privacy", "Spotlight"]
        )

        if mode == 'Privacy':
            output = img.copy()

            for (x, y, w, h) in faces:
                face_roi = output[y:y+h, x:x+w]
                blurred_face = cv2.GaussianBlur(face_roi, (51, 51), 0)
                output[y:y+h, x:x+w] = blurred_face

        else:
            blurred = cv2.GaussianBlur(img, (51, 51), 0)
            mask = np.zeros(img.shape[:2], dtype=np.uint8)

            for (x, y, w, h) in faces:
                cv2.rectangle(mask, (x, y), (x+w, y+h), 255, -1)

            output = np.where(mask[..., None] == 255, img, blurred)

        st.image(
            cv2.cvtColor(output, cv2.COLOR_BGR2RGB),
            caption="Result"
        )
