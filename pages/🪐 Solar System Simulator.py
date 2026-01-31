import streamlit as st
import matplotlib.pyplot as plt
import math
import random
from streamlit_autorefresh import st_autorefresh

st.title("🪐 Solar System Simulator")
st.subheader("Drag the slider and watch the planets spin!")

planets = {
    'Mercury': (1.0, 40, 'grey'),
    'Venus': (1.4, 90, 'brown'),
    'Earth': (1.8, 100, 'blue'),
    'Mars': (2.3, 55, 'red'),
    'Jupiter': (3.5, 300, 'orange'),
    'Saturn': (4.5, 260, '#d2b48c'),
    'Uranus': (5.5, 180, 'cyan'),
    'Neptune': (6.5, 175, 'blue'),
}

periods = {
    "Mercury": 88,
    "Venus": 225,
    "Earth": 365,
    "Mars": 687,
    "Jupiter": 4333,
    "Saturn": 10759,
    "Uranus": 30687,
    "Neptune": 60190,
}

moon = {
    'radius': 0.4,
    'size': 25,
    'color': 'lightgrey'
}

if 'phases' not in st.session_state:
    st.session_state.phases = {
        "Mercury": random.uniform(0, 2*math.pi),
        "Venus": random.uniform(0, 2*math.pi),
        "Earth": random.uniform(0, 2*math.pi),
        "Mars": random.uniform(0, 2*math.pi),
        "Jupiter": random.uniform(0, 2*math.pi),
        "Saturn": random.uniform(0, 2*math.pi),
        "Uranus": random.uniform(0, 2*math.pi),
        "Neptune": random.uniform(0, 2*math.pi),
    }

if 'autotime' not in st.session_state:
    st.session_state.autotime = 0

if "speed" not in st.session_state:
    st.session_state.speed = 20


auto = st.checkbox("Spin automatically", value=False)
if auto:
    st.session_state.speed = st.slider(
        "Simulation speed (days per tick)",
        1, 200,
        st.session_state.speed
    )

    st.session_state.autotime += st.session_state.speed

else:
    t = st.slider("Day", 0, 5000, 0)

show_labels = st.checkbox("Show labels", value=False)

zoom = st.slider("Zoom", 3,10,5,1)

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_autoscale_on(False)


ax.scatter(0, 0, s=900, color="yellow")
ax.text(-0.13, -0.07, "Sun", color="black", fontsize=9)

def in_view(x, y, z):
    return -z < x < z and -z < y < z

for name, (r, size, color) in planets.items():
    P = periods[name]
    if auto:
        angle = 2 * math.pi * st.session_state.autotime / P + st.session_state.phases[name]
    else:
        angle = 2 * math.pi * t / P + st.session_state.phases[name]

    x = r * math.cos(angle)
    y = r * math.sin(angle)

    orbit = plt.Circle((0, 0), r, color='white', alpha=0.08, fill=False)
    ax.add_patch(orbit)

    ax.scatter(x, y, s=size, color=color)
    if show_labels:
        ax.text(x+0.15, y+0.15, name, color="white", fontsize=8, clip_on=True)

    if name == "Earth":
        earth_angle = angle
        Ex, Ey = x, y

if auto:
    moon_angle = earth_angle + 2 * math.pi * st.session_state.autotime / 27
else:
    moon_angle = earth_angle + 2 * math.pi * t / 27
Mx = Ex + moon['radius'] * math.cos(moon_angle)
My = Ey + moon['radius'] * math.sin(moon_angle)

ax.scatter(Mx, My, s=moon['size'], color=moon['color'])
moon_orbit = plt.Circle(
    (Ex, Ey),
    moon['radius'],
    color='white',
    alpha=0.25,
    fill=False,
    linewidth=1
)
ax.add_patch(moon_orbit)

actual_zoom = 13-zoom

if show_labels and in_view(Mx, My, actual_zoom):
    ax.text(Mx, My, "Moon", color="white", fontsize=7)


ax.set_facecolor("black")
fig.patch.set_facecolor("black")

ax.set_aspect('equal')
ax.set_xlim(-actual_zoom , actual_zoom )
ax.set_ylim(-actual_zoom , actual_zoom )

ax.axis("off")

st.pyplot(fig)

if auto:
    st_autorefresh(interval=500, key='refresh')