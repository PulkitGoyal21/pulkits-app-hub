import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("Temperature gradient calculator")

labels = [
    "Corner (+1,+1,+1)",
    "Corner (-1,+1,+1)",
    "Corner (-1,-1,+1)",
    "Corner (+1,-1,+1)",
    "Corner (+1,+1,-1)",
    "Corner (-1,+1,-1)",
    "Corner (-1,-1,-1)",
    "Corner (+1,-1,-1)",
    "Center (0,0,0)"
]

cols = st.columns(3)
temps = []

for i, label in enumerate(labels):
    with cols[i % 3]:
        temps.append(
            st.slider(label, 0.0, 100.0, 25.0, 0.5)
        )

temps = np.array(temps)


points = np.array([
    [ 1,  1,  1],
    [-1,  1,  1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 0,  0,  0]
])

X = np.column_stack([
    points[:,0]**2,
    points[:,1]**2,
    points[:,2]**2,
    points[:,0]*points[:,1],
    points[:,1]*points[:,2],
    points[:,2]*points[:,0],
    points[:,0],
    points[:,1],
    points[:,2],
    np.ones(len(points))
])

coeffs = np.linalg.lstsq(X, temps, rcond=None)[0]
a,b,c,d,e,f,g,h,i,j = coeffs

def grad_T(x,y,z):
    dTdx = 2*a*x + d*y + f*z + g
    dTdy = 2*b*y + d*x + e*z + h
    dTdz = 2*c*z + e*y + f*x + i
    return dTdx, dTdy, dTdz

#z=0
x = np.linspace(-1, 1, 20)
y = np.linspace(-1, 1, 20)
Xg, Yg = np.meshgrid(x, y)

z = st.slider("z slice", -1.0, 1.0, 0.0, 0.1)

Zg = z

T = (
    a*Xg**2 + b*Yg**2 + c*Zg**2
    + d*Xg*Yg + e*Yg*Zg + f*Zg*Xg
    + g*Xg + h*Yg + i*Zg + j
)

dTdx, dTdy, _ = grad_T(Xg, Yg, Zg)

fig, ax = plt.subplots()

ax.contourf(Xg, Yg, T, cmap="inferno")
ax.quiver(Xg, Yg, dTdx, dTdy, color="white")
fig.colorbar(ax.collections[0], ax=ax, label="Temperature")

ax.set_xlabel("x")
ax.set_ylabel("y")

st.pyplot(fig)

T1, T2, T3, T4, T5, T6, T7, T8, Tc = temps

dTdxfull = (T1+T4+T5+T8-T2-T3-T6-T7)/8
dTdyfull = (T1+T2+T5+T6-T4-T3-T8-T7)/8
dTdzfull = (T1+T2+T3+T4-T5-T8-T6-T7)/8

st.divider()
st.latex(
    rf"\nabla T = {dTdxfull:.3f}\,\hat{{i}} + {dTdyfull:.3f}\,\hat{{j}} + {dTdzfull:.3f}\,\hat{{k}}"
)
st.latex(
    rf"|\nabla T| = {np.sqrt(dTdxfull**2 + dTdyfull**2 + dTdzfull**2):.3f}"
)


st.divider()
base_mag = np.sqrt(dTdxfull**2 + dTdyfull**2 + dTdzfull**2)

sens = []
delta = 1.0

for k in range(8):  # corners only
    T_mod = temps.copy()
    T_mod[k] += delta

    T1,T2,T3,T4,T5,T6,T7,T8,_ = T_mod

    dx = (T1+T4+T5+T8 - T2-T3-T6-T7)/8
    dy = (T1+T2+T5+T6 - T4-T3-T8-T7)/8
    dz = (T1+T2+T3+T4 - T5-T6-T7-T8)/8

    mag = np.sqrt(dx**2 + dy**2 + dz**2)
    sens.append(mag - base_mag)

fig, ax = plt.subplots()
ax.bar(range(1,9), sens)
ax.set_xlabel("Corner index")
ax.set_ylabel("Δ|∇T| per +1°C")
ax.set_title("Sensitivity of gradient magnitude")
st.pyplot(fig)
