import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Smart Energy Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Top Consumers", "Trends", "Export"])

# Dummy device metrics
device_metrics = {
    "A.C": {"usage": 2.4, "cost": 19.2, "status": "High"},
    "Heater": {"usage": 2.1, "cost": 16.8, "status": "High"},
    "Fridge": {"usage": 1.9, "cost": 15.2, "status": "Medium"},
    "Fan": {"usage": 0.8, "cost": 6.4, "status": "Low"},
    "Mixer": {"usage": 0.5, "cost": 4.0, "status": "Low"},
    "Light": {"usage": 0.6, "cost": 4.8, "status": "Low"},
    "Mobile": {"usage": 0.3, "cost": 2.4, "status": "Low"},
}

status_order = {"High": 0, "Medium": 1, "Low": 2}
sorted_devices = sorted(device_metrics.items(), key=lambda x: status_order[x[1]["status"]])

# Overview Page
if page == "Overview":
    st.title("⚡ Smart Energy Dashboard")
    st.markdown("Welcome to your enterprise-style energy monitoring system.")
    st.metric("Total Energy ⚡", "10.7 kWh")
    st.metric("Monthly Cost 💰", "₹85.6")

# Top Consumers Page
elif page == "Top Consumers":
    st.title("🔌 Top Energy Consumers")
    cols = st.columns(4)
    for i, (device, data) in enumerate(sorted_devices):
        bg = "#fff1f0" if data["status"] == "High" else "#fffbe6" if data["status"] == "Medium" else "#f6ffed"
        txt = "#d4380d" if data["status"] == "High" else "#d4b106" if data["status"] == "Medium" else "#389e0d"

        # Icons
        usage_icon = "⚡"
        cost_icon = "💰"
        status_icon = "📊"

        with cols[i % 4]:
            if st.button(f"{device}", key=f"tile_{device}"):
                st.session_state.selected_device = device
            st.markdown(f"""
                <div style='background:{bg}; padding:12px; border-radius:10px; text-align:center; border:1px solid #ccc; margin-top:5px;'>
                    <b style='color:{txt}; font-size:16px;'>{device}</b><br>
                    <span style='font-size:14px;'>{usage_icon} {data['usage']} kWh</span><br>
                    <span style='font-size:14px;'>{cost_icon} ₹{data['cost']}</span><br>
                    <span style='font-size:12px; color:{txt};'>{status_icon} Status: {data['status']}</span>
                </div>
            """, unsafe_allow_html=True)

        # Inline details below tile
        if st.session_state.get("selected_device") == device:
            st.markdown(f"##### 🔍 {device} Usage Details")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Usage ⚡", f"{data['usage']:.2f} kWh")
            col2.metric("Current Cost 💰", f"₹{data['cost']:.2f}")
            col3.metric("Weekly Total 📅", f"{data['usage']*6:.2f} kWh")
            col4.metric("Monthly Total 📅", f"{data['usage']*24:.2f} kWh")

            st.markdown("💡 **Recommendations:**")
            if data["status"] == "High":
                st.markdown("- Reduce usage during peak hours")
                st.markdown("- Upgrade to energy-efficient models")
            elif data["status"] == "Medium":
                st.markdown("- Monitor usage trends weekly")
            else:
                st.markdown("- Usage is optimal. No action needed.")

# Trends Page
elif page == "Trends":
    st.title("📈 Energy Trends")
    st.markdown("Charts and analytics go here.")
    df = pd.DataFrame({
        "Device": ["A.C", "Heater", "Fridge", "Fan"],
        "Usage": [2.4, 2.1, 1.9, 0.8]
    })
    fig = px.bar(df, x="Device", y="Usage", color="Device", title="Device Usage Comparison")
    st.plotly_chart(fig, use_container_width=True)

# Export Page
elif page == "Export":
    st.title("📥 Export Data")
    st.markdown("Download your energy usage summary.")
    df = pd.DataFrame(device_metrics).T
    csv = df.to_csv().encode("utf-8")
    st.download_button("Download Summary as CSV", csv, "summary.csv", "text/csv")

# Footer
st.markdown("""
    <hr style="margin-top:40px;">
    <div style="text-align:center; color:gray; font-size:14px;">
        © 2025 Smart Energy Dashboard | Built by Santosh Abhimanyu
    </div>
""", unsafe_allow_html=True)