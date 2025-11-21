import streamlit as st
import pandas as pd
from datetime import datetime
from src.agent import WaterAgent
from src.database import log_intake, get_intake

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

# First Section

if not st.session_state.tracker_started:
    st.title("Welcome to AI Suggester")
    st.markdown("""
                Some Para
                """)

    if st.button("Start Tracking"):
        st.session_state.tracker_started = True 
        st.experimental_rerun()

else:
    st.title("AI Dashboard")

    st.sidebar.header("Log Your Water Intake")
    user_id = st.sidebar.text_input("User ID", value="user_123")
    intake_ml = st.sidebar.number_input("Water Intake (ml)", min_value=0, step=100)

    if st.sidebar.button("Submit"):
        if user_id and intake_ml:
            log_intake(user_id, intake_ml)

            st.success(f"Logged {intake_ml} ml for {user_id}")

            agent = WaterAgent()
            feedback = agent.analyze(intake_ml)
            st.info(f"AI Feedback: {feedback}")

    st.markdown("---")

    st.header("Water History")

    if user_id:
        history = get_intake(user_id=user_id)
        if history:
            dates = [datetime.strptime(row[1], "%Y-%m-%d") for row in history]
            values = [row[0] for row in history]
            times = [datetime.strptime(row[2], "%H:%M:%S").time() for row in history]

            df = pd.DataFrame({"Date": dates, "Time": times, "Water": values})

            st.dataframe(df)

