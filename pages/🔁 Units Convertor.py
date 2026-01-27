import streamlit as st
import requests

st.title("🔁 Units convertor")

col1, col2 = st.columns(2)

choice = st.selectbox("Choose category", ['Length', 'Mass', 'Temp', 'Time', 'Data', 'Currency'])

@st.cache_data
def get_currencies():
    url = "https://open.er-api.com/v6/latest/USD"
    data = requests.get(url).json()
    return sorted(data["rates"].keys())

currencies = get_currencies()

len_factors = {
    "Meter (m)": 1.0,
    "Kilometer (km)": 1000.0,
    "Centimeter (cm)": 0.01,
    "Millimeter (mm)": 0.001,
    "Inch (in)": 0.0254,
    "Foot (ft)": 0.3048,
    "Mile (mi)": 1609.34
}

mass_factors = {
    "Kilogram (kg)": 1.0,
    "Gram (g)": 0.001,
    "Milligram (mg)": 0.000001,
    "Tonne (t)": 1000.0,
    "Pound (lb)": 0.45359237,
    "Ounce (oz)": 0.0283495231
}

time_factors = {
    "Second (s)": 1.0,
    "Minute (min)": 60.0,
    "Hour (h)": 3600.0,
    "Day (d)": 86400.0,
    "Week (wk)": 604800.0
}

data_factors = {
    "Byte (B)": 1,
    "Kilobyte (KB)": 1024,
    "Megabyte (MB)": 1024**2,
    "Gigabyte (GB)": 1024**3,
    "Terabyte (TB)": 1024**4,
    "Bit (b)": 1/8
}

if choice == 'Length':
    value = st.number_input("Enter value", value=1.0)

    from_unit = st.selectbox("From", len_factors.keys())
    to_unit = st.selectbox("To", len_factors.keys())

    m = value*len_factors[from_unit]
    result = m/len_factors[to_unit]

    st.success(f"{value} {from_unit} = {result:.6g} {to_unit}")

elif choice == 'Mass':
    value = st.number_input("Enter value", value=1.0)

    from_unit = st.selectbox("From", mass_factors.keys())
    to_unit = st.selectbox("To", mass_factors.keys())

    m = value*mass_factors[from_unit]
    result = m/mass_factors[to_unit]

    st.success(f"{value} {from_unit} = {result:.6g} {to_unit}")

elif choice == 'Temp':
    value = st.number_input("Enter value", value=1.0)

    from_unit = st.selectbox("From", ['Fahrenheit (°F)', 'Celsius (°C)', 'Kelvin (K)'])
    to_unit = st.selectbox("To", ['Fahrenheit (°F)', 'Celsius (°C)', 'Kelvin (K)'])

    result = value
    if from_unit == 'Fahrenheit (°F)':
        result = (result-32)*5/9
    elif from_unit == 'Kelvin (K)':
        result = result-273.15

    if to_unit == 'Fahrenheit (°F)':
        result = result*9/5+32
    elif to_unit == 'Kelvin (K)':
        result = result+273.15

    st.success(f"{value} {from_unit} = {result:.6g} {to_unit}")

elif choice == 'Time':
    value = st.number_input("Enter value", value=1.0)

    from_unit = st.selectbox("From", time_factors.keys())
    to_unit = st.selectbox("To", time_factors.keys())

    m = value*time_factors[from_unit]
    result = m/time_factors[to_unit]

    st.success(f"{value} {from_unit} = {result:.6g} {to_unit}")

elif choice == 'Data':
    value = st.number_input("Enter value", value=1.0)

    from_unit = st.selectbox("From", data_factors.keys())
    to_unit = st.selectbox("To", data_factors.keys())

    m = value*data_factors[from_unit]
    result = m/data_factors[to_unit]

    st.success(f"{value} {from_unit} = {result:.6g} {to_unit}")

elif choice == 'Currency':
    st.markdown("This idea was given by my close friend, RG. Credit to him!")
    amount = st.number_input("Enter amount", value=1.0)

    from_cur = st.selectbox("From", currencies, index=currencies.index("USD"))
    to_cur = st.selectbox("To", currencies, index=currencies.index("INR"))

    if st.button("Convert 🔁"):
        url = f"https://open.er-api.com/v6/latest/{from_cur}"
        data = requests.get(url).json()
        rate = data["rates"][to_cur]

        result = amount * rate
        st.success(f"{amount} {from_cur} = {result:.2f} {to_cur}")
