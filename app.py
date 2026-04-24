import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import cv2

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="Insider Threat Detection", layout="wide")

st.title("🔐 Insider Threat Detection System")

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("final_results.csv")

# ===============================
# COLOR FUNCTION
# ===============================
def color_risk(val):
    if val == "High":
        return "background-color: red; color: white"
    elif val == "Medium":
        return "background-color: orange"
    else:
        return "background-color: green; color: white"

# ===============================
# SIDEBAR
# ===============================
st.sidebar.header("📷 Camera Control")
run_camera = st.sidebar.checkbox("Enable Camera")

# ===============================
# FACE DETECTION
# ===============================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

placeholder = st.empty()

# ===============================
# MAIN LOOP
# ===============================
while True:

    sample = df.sample(50)
    sample["total_files_burned"] += np.random.randint(0, 5, size=50)

    risk_counts = sample["Risk_Level"].value_counts()

    with placeholder.container():

        # ===============================
        # CAMERA SECTION
        # ===============================
        user_present = False

        if run_camera:
            st.subheader("📷 Camera Monitoring")

            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()

            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

                st.image(frame, channels="BGR")

                user_present = len(faces) > 0

            cap.release()

        # ===============================
        # ROLE-BASED ACCESS
        # ===============================
        if run_camera:
            if user_present:
                role = "Admin"
                st.success("👑 Admin Verified - Full Access")
            else:
                role = "Viewer"
                st.warning("👤 Viewer Mode - Limited Access")
        else:
            role = "Viewer"
            st.info("Camera Off - Viewer Mode")

        # ===============================
        # SMART ALERT
        # ===============================
        high_risk_users = sample[sample["Risk_Level"] == "High"]

        if role == "Viewer" and len(high_risk_users) > 0:
            st.error("🚨 ALERT: High Risk Activity Detected!")

        # ===============================
        # DASHBOARD BASED ON ROLE
        # ===============================
        if role == "Admin":

            col1, col2 = st.columns(2)

            # 📊 Chart
            with col1:
                st.subheader("📊 Risk Distribution")
                fig, ax = plt.subplots()
                ax.bar(risk_counts.index, risk_counts.values)
                ax.set_title("Risk Levels")
                st.pyplot(fig)

            # 🚨 Alerts
            with col2:
                st.subheader("🚨 High Risk Alerts")
                high = sample[sample["Risk_Level"] == "High"]
                st.dataframe(
                    high.style.applymap(color_risk, subset=["Risk_Level"]),
                    use_container_width=True
                )

            # 📋 Full data
            st.subheader("📋 Full User Activity")
            st.dataframe(
                sample.style.applymap(color_risk, subset=["Risk_Level"]),
                use_container_width=True
            )

        else:
            # LIMITED VIEW
            st.subheader("📊 Risk Overview")
            st.bar_chart(risk_counts)

            st.warning("⚠️ Detailed data restricted to Admin")

    time.sleep(3)