import streamlit as st
import time
import math

st.set_page_config(page_title="Number Personality AI", layout="centered")
st.title("🔢 Number Personality Analyzer")

def smooth_step(bar, status, pct, text, delay=0.25):
    status.text(text)
    bar.progress(pct)
    time.sleep(delay)


num = st.number_input(
    "Enter a number",
    min_value=0,
    max_value=10**8 - 1,
    step=1
)

if num >= 10**8:
    st.error("Computational nightmare. Impossible to calculate.")
    st.stop()

ops = 0

POSITIVITY_PHRASES = {
    0: "Pure negativity. Cursed energy.",
    5: "Perfectly neutral. Balanced.",
    10: "Pure goodness. Blessed number."
}

COMPLEXITY_PHRASES = {
    0: "Trivial. Instant result.",
    5: "Moderately complex.",
    10: "Computational nightmare."
}

RARITY_PHRASES = {
    0: "Common as dust.",
    5: "Moderately rare.",
    8: "Elite rarity. Tiny club.",
    10: "Unique-tier. One-of-a-kind energy."
}

RARITY_ORDER = [
    "deficient",
    "harshad",
    "palindrome",
    "semiperfect",
    "abundant",
    "prime",
    "happy",
    "armstrong",
    "weird",
    "perfect"
]

unhappy_list = [4, 16, 37, 58, 89, 145, 42, 20]

# ---------- FUNCTIONS (UNCHANGED LOGIC) ----------

def happy(n):
    global ops
    s = 0
    while n > 0:
        ops += 1
        s += (n % 10) ** 2
        n //= 10
    return s

def is_happy(n):
    global ops
    if n in (0, 1):
        return False
    while True:
        ops += 1
        n = happy(n)
        if n == 1:
            return True
        if n in unhappy_list:
            return False

def get_factors(n):
    global ops
    if n <= 1:
        return []
    f = [1]
    for i in range(2, int(n**0.5) + 1):
        ops += 1
        if n % i == 0:
            f.append(i)
            if i != n // i:
                f.append(n // i)
    return f

def ai_comment(r, c, p):
    if r >= 8 and c >= 8 and p >= 7:
        return "Legendary number. Rare, powerful, and demanding to analyze."
    if p >= 8 and r < 4:
        return "Strong positive vibes, but structurally common."
    if c >= 8 and p <= 3:
        return "Cursed behavior detected. Painful to analyze."
    if r <= 2 and c <= 2:
        return "NPC-tier number."
    return "Balanced number. Nothing extreme."

# ---------- RUN ----------

if st.button("Analyze 🔥"):
    status = st.empty()
    bar = st.progress(0)

    start = time.perf_counter()

    status.text("Finding factors…")
    factors = get_factors(num)
    bar.progress(20)

    status.text("Checking happiness…")
    happy_flag = is_happy(num)
    bar.progress(40)

    status.text("Evaluating traits…")
    personality = {
        "happy": happy_flag,
        "prime": len(factors) == 1,
        "perfect": sum(factors) == num and num != 0,
        "abundant": sum(factors) > num,
        "deficient": sum(factors) < num if num != 0 else False,
        "palindrome": str(num) == str(num)[::-1],
        "harshad": num != 0 and num % sum(map(int, str(num))) == 0,
        "armstrong": num == sum(int(d)**len(str(num)) for d in str(num)),
        "semiperfect": False,
        "weird": False
    }
    smooth_step(bar, status, 75, "Scoring number personality…")

    end = time.perf_counter()
    time_taken = end - start

    smooth_step(bar, status, 100, "Finalizing results…", delay=0.4)
    status.success("Done ✅")

    GOOD_SET = ["happy", "perfect", "abundant"]
    MID_SET = ["semiperfect", "harshad", "palindrome", "prime"]
    BAD_SET = ["deficient", "weird", "armstrong"]

    good = sum(personality[x] is True for x in GOOD_SET) + \
           sum(personality[x] is False for x in BAD_SET)
    mid = sum(personality[x] is True for x in MID_SET)
    bad = sum(personality[x] is True for x in BAD_SET) + \
          sum(personality[x] is False for x in GOOD_SET)

    positivity = 1.5 + good*2 + mid*1 - bad*0.5
    positivity = max(0, min(10, round(positivity*2)/2))

    time_score = min((time_taken * 1000) / 0.8, 1)
    ops_score = min(ops / 1500, 1)
    complexity = round((time_score*0.5 + ops_score*0.5) * 10 * 2) / 2

    rarity = 0
    for k, v in personality.items():
        if v is True:
            rarity += RARITY_ORDER.index(k) + 1
    rarity = round((rarity / 55) * 10)

    bar.progress(100)
    status.success("Done ✅")

    # ---------- OUTPUT ----------

    st.subheader("📊 Traits")
    for k, v in personality.items():
        st.write(("🔥" if v else "❌") + f" **{k}**")

    st.subheader("🧠 Ratings")
    st.metric("Positivity", f"{positivity}/10")
    st.metric("Complexity", f"{complexity}/10")
    st.metric("Rarity", f"{rarity}/10")

    st.subheader("🤖 Final Verdict")
    st.success(ai_comment(rarity, complexity, positivity))

    st.caption(f"Ops: {ops} | Time: {time_taken:.6f}s")
