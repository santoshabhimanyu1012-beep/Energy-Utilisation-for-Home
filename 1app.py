import streamlit as st

# Page setup
st.set_page_config(page_title="Smart Energy Dashboard", layout="wide")

# Load custom CSS theme
st.markdown(f"<style>{open('theme.css').read()}</style>", unsafe_allow_html=True)

# Device metrics
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

# Render tiles and inline details
cols = st.columns(4)
for i, (device, data) in enumerate(sorted_devices):
    bg = "#fff1f0" if data["status"] == "High" else "#fffbe6" if data["status"] == "Medium" else "#f6ffed"
    txt = "#d4380d" if data["status"] == "High" else "#d4b106" if data["status"] == "Medium" else "#389e0d"
    with cols[i % 4]:
        if st.button(f"{device}", key=f"tile_{device}"):
            st.session_state.selected_device = device
        st.markdown(f"""
            <div style='background:{bg}; padding:12px; border-radius:10px; text-align:center; border:1px solid #ccc; margin-top:5px;'>
                <b style='color:{txt}; font-size:16px;'>{device}</b><br>
                <span style='font-size:14px;'>{data['usage']} kWh</span><br>
                <span style='font-size:14px;'>₹{data['cost']}</span><br>
                <span style='font-size:12px; color:{txt};'>Status: {data['status']}</span>
            </div>
        """, unsafe_allow_html=True)

        # Inline details below tile
        if st.session_state.get("selected_device") == device:
            st.markdown(f"##### 🔍 {device} Usage Details")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Usage", f"{data['usage']:.2f} kWh")
            col2.metric("Current Cost", f"₹{data['cost']:.2f}")
            col3.metric("Weekly Total", f"{data['usage']*6:.2f} kWh")
            col4.metric("Monthly Total", f"{data['usage']*24:.2f} kWh")

            st.markdown("💡 **Recommendations:**")
            if data["status"] == "High":
                st.markdown("- Reduce usage during peak hours")
                st.markdown("- Upgrade to energy-efficient models")
            elif data["status"] == "Medium":
                st.markdown("- Monitor usage trends weekly")
            else:
                st.markdown("- Usage is optimal. No action needed.")

# Footer
st.markdown("""
    <hr style="margin-top:40px;">
    <div style="text-align:center; color:gray; font-size:14px;">
        © 2025 Smart Energy Dashboard | Built by Santosh Abhimanyu
    </div>
""", unsafe_allow_html=True)