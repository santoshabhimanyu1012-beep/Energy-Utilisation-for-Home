import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Smart Energy Dashboard", layout="wide")

# Load custom CSS theme
st.markdown(f"<style>{open('theme.css').read()}</style>", unsafe_allow_html=True)

# Top navigation bar
st.markdown("""
    <div style='display:flex; justify-content:space-between; align-items:center; background:#f0f2f6; padding:10px 20px; border-radius:8px;'>
        <div style='display:flex; gap:20px; font-weight:bold; font-size:18px;'>
            <span>🏠 Home</span>
            <span>⚡ Total Energy: <b>4.79 kWh</b></span>
            <span>💰 Monthly Cost: <b>₹38.32</b></span>
        </div>
        <div>
            <button style='background:#3498db; color:white; border:none; padding:6px 12px; border-radius:6px;'>Login / Sign In</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.header("🔧 Filters")
    device_type = st.selectbox("Device Type", ["All", "Fan", "Light", "Fridge", "TV"])
    time_granularity = st.selectbox("Time View", ["Hourly", "Daily", "Weekly", "Monthly"])
    tariff = st.number_input("Tariff (₹ per kWh)", min_value=0.0, value=8.0, step=0.5)
    data_option = st.radio("Data Source", ["Upload CSV", "Use Sample"])
    uploaded = None
    if data_option == "Upload CSV":
        uploaded = st.file_uploader("Upload CSV", type=["csv"])

# Load data
if data_option == "Upload CSV" and uploaded:
    df = pd.read_csv(uploaded)
elif data_option == "Use Sample":
    df = pd.DataFrame({
        "Timestamp": [
            "2025-12-26 08:00","2025-12-26 09:00","2025-12-26 10:00",
            "2025-12-26 11:00","2025-12-26 12:00","2025-12-26 13:00",
            "2025-12-26 14:00","2025-12-26 15:00","2025-12-26 16:00"
        ],
        "Fan (W)": [120,100,130,90,110,95,105,115,98],
        "Light (W)": [60,40,70,50,65,55,45,60,52],
        "Fridge (W)": [200,220,210,230,205,215,225,210,220],
        "TV (W)": [150,160,140,170,155,145,165,150,160]
    })
else:
    st.info("Upload a CSV to proceed or switch to Sample CSV.")
    st.stop()

# Validate and preprocess
if "Timestamp" not in df.columns:
    st.error("CSV must include a 'Timestamp' column.")
    st.stop()

df["Timestamp"] = pd.to_datetime(df["Timestamp"])
device_cols = [c for c in df.columns if c != "Timestamp"]
if not device_cols:
    st.error("CSV must include device columns like 'Fan (W)', 'Fridge (W)', etc.")
    st.stop()

# Filter by device type
if device_type != "All":
    device_cols = [col for col in device_cols if device_type in col]
    if not device_cols:
        st.warning(f"No data found for {device_type}")
        st.stop()

# Aggregate by time view
work = df.copy().set_index("Timestamp")
if time_granularity == "Hourly":
    agg = work.resample("H").mean()
elif time_granularity == "Daily":
    agg = work.resample("D").mean()
elif time_granularity == "Weekly":
    agg = work.resample("W").mean()
else:
    agg = work.resample("M").mean()

# Totals
kwh_per_device = (work[device_cols].sum()) / 1000.0
costs = kwh_per_device * tariff
total_kwh = kwh_per_device.sum()
total_cost = costs.sum()

# KPI cards
st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col1.metric("🔌 Total kWh", f"{total_kwh:.2f}")
col2.metric("💰 Estimated Cost", f"₹{total_cost:.2f}")
col3.metric("📁 Records", f"{len(df)} rows")
st.markdown("</div>", unsafe_allow_html=True)

# Device breakdown table
st.subheader("📊 Device Breakdown")
summary = pd.DataFrame({
    "Total kWh": kwh_per_device.round(3),
    "Estimated Cost (INR)": costs.round(2)
})
st.dataframe(summary, use_container_width=True)

# SAP-style Tiles for Top Energy Consumers
st.subheader("🔌 Top Energy Consumers")

device_metrics = {
    "A.C": {"usage": 2.4, "cost": 19.2, "status": "High"},
    "Fridge": {"usage": 1.9, "cost": 15.2, "status": "Medium"},
    "Fan": {"usage": 0.8, "cost": 6.4, "status": "Low"},
    "Heater": {"usage": 2.1, "cost": 16.8, "status": "High"},
    "Mixer": {"usage": 0.5, "cost": 4.0, "status": "Low"},
    "Light": {"usage": 0.6, "cost": 4.8, "status": "Low"},
    "Mobile": {"usage": 0.3, "cost": 2.4, "status": "Low"},
}

selected_device = None
cols = st.columns(4)
for i, (device, data) in enumerate(device_metrics.items()):
    color = "#e74c3c" if data["status"] == "High" else "#f1c40f" if data["status"] == "Medium" else "#2ecc71"
    with cols[i % 4]:
        if st.button(f"{device}", key=device):
            selected_device = device
        st.markdown(f"""
            <div style='background:{color}; padding:10px; border-radius:8px; color:white; text-align:center; margin-top:5px;'>
                <b>{device}</b><br>
                {data['usage']} kWh<br>
                ₹{data['cost']}<br>
                <span style='font-size:12px;'>Status: {data['status']}</span>
            </div>
        """, unsafe_allow_html=True)

# Show details if a tile is clicked
if selected_device:
    data = device_metrics[selected_device]
    st.markdown(f"### 🔍 {selected_device} Usage Details")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Usage", f"{data['usage']:.2f} kWh")
    col2.metric("Current Cost", f"₹{data['cost']:.2f}")
    col3.metric("Weekly Total", f"{data['usage']*6:.2f} kWh")
    col4.metric("Monthly Total", f"{data['usage']*24:.2f} kWh")

    st.markdown("📊 Weekly Change: **+12%**")
    st.markdown("📊 Monthly Change: **-5%**")

    st.markdown("💡 **Recommendations:**")
    if data["status"] == "High":
        st.markdown("- Consider reducing usage during peak hours")
        st.markdown("- Explore energy-efficient alternatives")
    else:
        st.markdown("- Usage is within optimal range")

# Visual Trends
st.subheader("📈 Visual Trends")
tab1, tab2, tab3 = st.tabs(["Line Chart", "Bar Chart", "Pie Chart"])
with tab1:
    fig_line = px.line(agg.reset_index(), x="Timestamp", y=device_cols,
                       labels={"value":"Power (W)","variable":"Device"})
    st.plotly_chart(fig_line, use_container_width=True)
with tab2:
    fig_bar = px.bar(x=kwh_per_device.index, y=kwh_per_device.values,
                     labels={"x":"Device","y":"Total kWh"})
    st.plotly_chart(fig_bar, use_container_width=True)
with tab3:
    fig_pie = px.pie(values=kwh_per_device.values, names=kwh_per_device.index)
    st.plotly_chart(fig_pie, use_container_width=True)

# Export Summary
st.subheader("📥 Export Summary")
csv = summary.to_csv().encode("utf-8")
st.download_button("Download Summary as CSV", csv, "summary.csv", "text/csv")

# Footer
st.markdown("""
    <hr style