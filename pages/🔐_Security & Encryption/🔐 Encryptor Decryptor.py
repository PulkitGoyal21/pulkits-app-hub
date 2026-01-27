import random
import streamlit as st
import time
from io import StringIO
from collections import deque

# ---------------- ENCRYPT ---------------- #

def encrypt(message, use_password, password_val=None):
    start = time.time()
    temp_msg = []
    new_msg = []
    letters = numbers = 0

    for ch in message:
        try:
            temp_msg.append(int(ch))
        except ValueError:
            temp_msg.append(ch)

    base = random.randint(2, 5)

    # password flag
    if use_password:
        new_msg.append(1)
        pwd = password_val
        while pwd > 0:
            new_msg.insert(1, pwd % base)
            pwd //= base
    else:
        new_msg.append(0)

    new_msg.append(5)

    base_map = {
        2: [0, 1, 0],
        3: [0, 1, 1],
        4: [1, 0, 0],
        5: [1, 0, 1],
    }
    new_msg.extend(base_map[base])
    new_msg.append(5)

    for item in temp_msg:
        if isinstance(item, str):
            letters += 1
            new_msg.append(1)
            val = ord(item)
        else:
            numbers += 1
            new_msg.append(0)
            val = item

        bin_list = []
        if val == 0:
            bin_list = [0]
        else:
            while val > 0:
                bin_list.insert(0, val % base)
                val //= base

        new_msg.extend(bin_list)
        new_msg.append(5)

    msg_str = ''.join(map(str, new_msg))
    altsum = sum(int(c) for c in msg_str)
    final = f"{altsum};{msg_str}"

    return {
        "encrypted": final,
        "letters": letters,
        "numbers": numbers,
        "base": base,
        "password": use_password,
        "time": round((time.time() - start) * 1000, 3),
        "altsum": altsum
    }


# ---------------- DECRYPT ---------------- #

def decrypt(encrypted, password_val=None):
    start = time.time()

    if ';' not in encrypted:
        return {"error": "Invalid encrypted format"}

    altsum_given, body = encrypted.split(';', 1)
    altsum_given = int(altsum_given)

    if sum(int(c) for c in body) != altsum_given:
        return {"error": "Tampering detected ❌"}

    message = deque(body)

    password_flag = message.popleft() == '1'

    # password check
    if password_flag:
        if password_val is None:
            return {"error": "Password required"}

        pwd_bits = []
        while message[0] != '5':
            i = message.popleft()
            pwd_bits.append(i)
        message.popleft()
    else:
        message.popleft()
        
    base_bits = [int(message.popleft()), int(message.popleft()), int(message.popleft())]
    base = base_bits[0]*4 + base_bits[1]*2 + base_bits[2]
    message.popleft()  # skip 5

    if password_flag:
        check = 0
        for d in pwd_bits:
            check = check * base + int(d)

        if check != password_val:
            return {"error": "Incorrect password ❌"}

        if base not in [2,3,4,5]:
            return {"error": "Invalid base"}

    decrypted = []
    temp_bin = []
    ischar = None

    if not message:
        return {"error": "Corrupt data"}

    ischar = message.popleft() == '1'

    while message:
        if message[0] != '5':
            temp_bin.append(message.popleft())
        else:
            message.popleft()

            value = 0
            for d in temp_bin:
                value = value * base + int(d)

            if ischar:
                decrypted.append(chr(value))
            else:
                decrypted.append(str(value))

            temp_bin.clear()

            if message:
                ischar = message.popleft() == '1'

    return {
        "decrypted": ''.join(decrypted),
        "time": round((time.time() - start) * 1000, 3),
        "base": base,
        "password": password_flag,
        "altsum": altsum_given
    }


# ---------------- STREAMLIT UI ---------------- #

st.title("🔐 Encryptor / Decryptor")

mode = st.radio("Choose mode", ["Encrypt", "Decrypt"])

# -------- ENCRYPT UI -------- #

if mode == "Encrypt":
    message = st.text_input("Enter message", "Top secret...")
    use_password = st.radio("Password based encryption?", ["Yes", "No"])

    password_val = None
    if use_password == "Yes":
        password_val = st.number_input("Numeric password", min_value=1, step=1)

    if st.button("Encrypt 🔒"):
        result = encrypt(message, use_password == "Yes", password_val)

        st.code(result["encrypted"])
        st.success("Encryption complete")

        st.write("Letters:", result["letters"])
        st.write("Numbers:", result["numbers"])
        st.write("Base:", result["base"])
        st.write("Password protected:", result["password"])
        st.write("Time (ms):", result["time"])
        st.write("Tamper checksum:", result["altsum"])

        st.download_button(
            "📄 Download encrypted file",
            result["encrypted"],
            file_name="encrypted.txt"
        )

# -------- DECRYPT UI -------- #

else:
    choice = st.radio("Choose mode", ["Upload .txt file", "Paste text"])
    if choice == "Paste text":
        encrypted_input = st.text_area("Paste encrypted message")
    elif choice == "Upload .txt file":
        uploaded_file = st.file_uploader("📄 Upload file", type=['txt'])
        if uploaded_file is not None:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            encrypted_input = stringio.read()

    password_val = st.number_input(
        "Password (leave 0 if none)",
        min_value=0,
        step=1
    )

    if st.button("Decrypt 🔓"):
        pwd = None if password_val == 0 else password_val
        result = decrypt(encrypted_input.strip(), pwd)

        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Decryption successful")
            st.code(result["decrypted"])

            st.write("Base:", result["base"])
            st.write("Password protected:", result["password"])
            st.write("Time (ms):", result["time"])
            st.write("Checksum:", result["altsum"])
