import streamlit as st
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import base64

with open("engine_idle_loop.wav", "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode()

with open("gear_shift.wav", "rb") as f:
    gear_b64 = base64.b64encode(f.read()).decode()

st.title('🏎️ Car Simulator')
st.markdown('Simulation of a real car based on speed, braking, gears and rpm.')

st.warning("⚠️ This is a demanding app and may not run smoothly on some devices")

idle_rpm = 900
redline = 8500
max_speed = 420

gear_ratios = [2.8, 2.1, 1.6, 1.25, 1.0, 0.82]
min_speed = [0, 35, 80, 140, 210, 280]
max_speed_gear = [90, 150, 220, 300, 360, 420]

if "t" not in st.session_state:
    st.session_state.t = []
    st.session_state.rpm_hist = []
    st.session_state.speed_hist = []
    st.session_state.ticky = 0

if "rpm" not in st.session_state:
    st.session_state.rpm = idle_rpm
    st.session_state.speed = 0.0
    st.session_state.gear = 1

rpm = st.session_state.rpm
speed = st.session_state.speed
gear = st.session_state.gear

if "last_gear" not in st.session_state:
    st.session_state.last_gear = gear

intent = st.radio(
    "Drive control",
    ["Coast", "Accelerate", "Brake"],
    horizontal=True
)

mode = st.radio("Performance mode", ['Normal', 'High (removes graphs)', 'Ultra (removes sound)'])

factor = 1
if mode != 'Normal':
    factor = 1
else:
    factor = 1
st_autorefresh(interval=600*factor, key='tick')


ratio = gear_ratios[gear - 1]

if intent == "Accelerate":
    rpm += 270*ratio*factor
    speed += 3.2 * ratio*factor

elif intent == "Brake":
    rpm -= 720*factor/ratio
    speed -= 9.2*factor

else:
    rpm -= 240*factor/ratio
    speed -= 0.26*factor

rpm = max(idle_rpm, min(rpm, redline))
speed = max(0, min(speed, max_speed))

if rpm >= 8200 and  gear < len(gear_ratios) and speed>max_speed_gear[gear-1]:
    rpm *= 0.5
    gear += 1
elif rpm <= 1800 and gear > 1 and speed<min_speed[gear-1]:
    rpm *= 1.9
    gear -= 1

st.session_state.rpm = rpm
st.session_state.speed = speed
st.session_state.gear = gear

speedometer = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=speed,
        number={'suffix': ' km/h'},
        gauge={
            'axis': {'range': [0, max_speed]},
            'bar': {'color': 'red' if rpm > 0.9 * redline else 'lime'},
            'steps': [
                {'range': [0, max_speed*0.5], 'color': '#1f1f1f'},
                {'range': [max_speed*0.5, max_speed*0.8], 'color': '#3a3a3a'},
                {'range': [max_speed*0.8, max_speed], 'color': '#5a0000'},
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': speed,
            }
        }
    )
)

speedometer.update_layout(
    height=300,
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="black",
    font={'color': "white"}
)

with st.container():
    st.plotly_chart(speedometer, use_container_width=True)

rpm_ratio = rpm / redline
st.progress(min(1.0, rpm_ratio))

if rpm_ratio > 0.85:
    st.markdown(
        """
        <style>
        /* Progress bar fill */
        div[data-testid="stProgress"] > div > div {
            background-color: #ff1a1a !important;
        }

        /* Progress bar track */
        div[data-testid="stProgress"] > div {
            background-color: #400000 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


if rpm_ratio > 0.85:
    st.markdown(
        """
        <style>
        div[data-testid="stProgress"] > div > div {
            background-color: red;
            animation: pulse 0.6s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


gear_changed = gear != st.session_state.last_gear
st.session_state.last_gear = gear

if gear_changed:
    st.markdown(
        """
        <style>
        .stApp {
            animation: flash 0.15s;
        }
        @keyframes flash {
            0% { background-color: #ffffff; }
            100% { background-color: #000000; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


danger = rpm > 0.9 * redline
if danger:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #3b0000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


st.metric("RPM", int(rpm))
st.metric("Speed", round(speed, 1))
st.metric("Gear", gear)

st.write("State:", intent)


if mode == 'Normal':
    st.session_state.ticky += 1

    st.session_state.t.append(st.session_state.ticky)
    st.session_state.rpm_hist.append(rpm)
    st.session_state.speed_hist.append(speed)

    MAX_POINTS = 50

    if len(st.session_state.t) > MAX_POINTS:
        st.session_state.t.pop(0)
        st.session_state.rpm_hist.pop(0)
        st.session_state.speed_hist.pop(0)


    c1, c2 = st.columns(2)

    c1.subheader("📈 RPM over time")
    c1.line_chart(
        {"RPM": st.session_state.rpm_hist},
        height=250
    )

    c2.subheader("📈 Speed over time")
    c2.line_chart(
        {"Speed": st.session_state.speed_hist},
        height=250
    )

if not mode == 'Ultra (removes sound)':
    st.components.v1.html(f"""
    <div style="display:none">
    <audio id="engine" loop>
        <source src="data:audio/wav;base64,{audio_b64}" type="audio/wav">
    </audio>
    </div>

    <script>
    if (!window.engineAudio) {{
        window.engineAudio = document.getElementById("engine");
        window.engineAudio.preservesPitch = false;
        window.engineAudio.play();
        window.engineAudio.smoothRate = 1.0;
    }}

    let rpm = {rpm};
    let idle = {idle_rpm};
    let redline = {redline};

    // map rpm → playbackRate (SAME LOGIC AS YOUR WORKING DEMO)
    let target = 0.8 + (rpm - idle) / (redline - idle) * 2.7;
    target = Math.min(3.2, Math.max(0.7, target));

    // smooth it
    window.engineAudio.smoothRate +=
        (target - window.engineAudio.smoothRate) * 0.06;

    window.engineAudio.playbackRate = window.engineAudio.smoothRate;
    </script>
    """, height=0)

    st.components.v1.html(f"""
    <div style="display:none">
    <audio id="gear-sound">
        <source src="data:audio/wav;base64,{gear_b64}" type="audio/wav">
    </audio>
    </div>

    <script>
    if (!window.gearAudio) {{
        window.gearAudio = document.getElementById("gear-sound");
        window.gearAudio.volume = 1.0;
    }}

    // Python tells us if gear changed
    let gearChanged = {str(gear_changed).lower()};

    if (gearChanged) {{
        window.gearAudio.currentTime = 0;
        window.gearAudio.play();
    }}
    </script>
    """, height=0)

