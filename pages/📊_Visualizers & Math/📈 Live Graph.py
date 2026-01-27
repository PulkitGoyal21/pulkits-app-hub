import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

flag = 0

st.title("Live Graph Plotter")
st.subheader("Zoom")
st.sidebar.subheader("🎚️ Degree")

zoom_factor = st.slider(
    "Zoom",
    min_value=0.5,
    max_value=10.0,
    value=1.0,
    step=0.1
)

base_range = 10        # your reference canvas
x_range = base_range / zoom_factor

x = np.linspace(-x_range, x_range, 2000)

st.divider()
st.subheader("Choose wave")

degree = st.sidebar.slider("Polynomial degree", min_value=1, max_value=7, value=2, step=1)
#st.sidebar().divider()

st.sidebar.subheader("🎛️ Coefficients")
coeffs = []
for i in range (degree,-1,-1):
    default = 1.0 if i == degree else 0.0
    coeff = st.sidebar.slider(f'Coefficient of x**{i}', min_value=-10.0, max_value=10.0, value=default, step=0.5)
    coeffs.append(coeff)

terms = []

for i, c in zip(range(degree, -1, -1), coeffs):
    if c == 0:
        continue

    if i == 0:
        terms.append(f"{c}")
    elif i == 1:
        terms.append(f"{c}x")
    else:
        terms.append(f"{c}x^{i}")

equation = " + ".join(terms)

if "wave" not in st.session_state:
    st.session_state.wave = "Custom (sidebar)"

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Own config**")
    if st.button("Custom (sidebar)", use_container_width=True):
        st.session_state.wave = "Custom (sidebar)"

with col2:
    st.markdown("**Trig ratios**")
    for opt in ["Sin", "Cos", "Tan", "Cosec", "Sec", "Cot"]:
        if st.button(opt, use_container_width=True):
            st.session_state.wave = opt

with col3:
    st.markdown("**Special graphs**")
    for opt in ["Sum of sines", "Chirp", "Damped", "Rational", "Chaos"]:
        if st.button(opt, use_container_width=True):
            st.session_state.wave = opt

st.info(f"Selected wave: {st.session_state.wave}")


if st.session_state.wave == "Custom (sidebar)":
    flag = 0

if st.session_state.wave == "Sin":
    flag = 1
    y = np.sin(x)
    equation = r"\sin(x)"

if st.session_state.wave == "Cos":
    flag = 1
    y = np.cos(x)
    equation = r"\cos(x)"

if st.session_state.wave == "Tan":
    flag = 1
    y = np.tan(x)
    y[np.abs(y) > 10] = np.nan
    equation = r"\tan(x)"

if st.session_state.wave == "Cosec":
    flag = 1
    y = 1/np.sin(x)
    y[np.abs(y) > 10] = np.nan
    equation = r"\csc(x)"

if st.session_state.wave == "Sec":
    flag = 1
    y = 1 / np.cos(x)
    y[np.abs(np.cos(x)) < 0.1] = np.nan
    equation = r"\sec(x)"

if st.session_state.wave == "Cot":
    flag = 1
    y = 1 / np.tan(x)
    y[np.abs(np.sin(x)) < 0.1] = np.nan
    equation = r"\cot(x)"

if st.session_state.wave=="Sum of sines":
    flag = 1
    y = np.sin(x) + 0.5*np.sin(3*x) + 0.25*np.sin(7*x)
    equation = r"\sin(x)+0.5\sin(3x)+0.25\sin(7x)"

if st.session_state.wave=="Chirp":
    flag = 1
    y = np.sin(x**2)
    equation = r"\sin(x^2)"


if st.session_state.wave=="Damped":
    flag = 1
    y = np.exp(-0.1*x) * np.sin(5*x)
    equation = r"e^{-0.1x}\sin(5x)"

if st.session_state.wave=="Rational":
    flag = 1
    y = np.sin(1 / np.where(x == 0, np.nan, x))
    equation = r"""
    \sin\!\left(\frac{1}{x}\right), \quad x \neq 0
    """

if st.session_state.wave=="Chaos":
    flag = 1
    y = np.sin(x) * np.cos(x**2)
    equation = r"\sin(x)\cos\!\left(x^2\right)"

st.latex(f"y = {equation}")

if flag == 0:
    y = np.zeros_like(x)
    for i, c in zip(range(degree, -1, -1), coeffs):
        y += c * x**i

fig, ax = plt.subplots()
ax.plot(x, y)
ax.axhline(0)   # x-axis
ax.axvline(0)   # y-axis
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_xlim(-x_range, x_range)
ax.set_title("Polynomial Graph")

st.pyplot(fig)