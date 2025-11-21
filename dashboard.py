import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from src.agent import WaterAgent
from src.database import log_intake, get_intake

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

# First Section

if not st.session_state.tracker_started:
    st.title("Welcome to AI Water Tracker!")
    st.markdown("""
                This your smart hydration companion. Track your daily water intake and view your hydration patterns. 
                With each water intake, you will receive personalized AI-powered suggestions to help you stay healthy and energized. 
                Log your sips throughout the day and let your hydration assistant keep you on track effortlessly. 
                """)

    if st.button("Start Tracking"):
        st.session_state.tracker_started = True 
        st.experimental_rerun()

else:
    st.title("AI Water Tracker Dashboard")

    st.header("Log Your Water Intake")
    user_id = st.text_input("User ID", value="user_123")
    intake_ml = st.number_input("Water Intake (ml)", min_value=0, step=100)

    if st.button("Submit"):
        if user_id and intake_ml:
            log_intake(user_id, intake_ml)

            # st.success(f"Logged {intake_ml} ml for {user_id}")

            agent = WaterAgent()
            feedback = agent.analyze(user_id)
            st.session_state.feedback = feedback

            st.markdown("AI Feedback:")
            st.markdown(f"{feedback}")

    st.markdown("---")

    if st.button("Show Water Patterns"):

        st.header("Water History")
        st.markdown("AI Feedback:")
        st.markdown(f"{st.session_state.feedback}")

        if user_id:
            history = get_intake(user_id=user_id)
            if history:
                col1, col2 = st.columns([1,1])
                dates = [datetime.strptime(row[1], "%Y-%m-%d") for row in history]
                values = [row[0] for row in history]
                times = [datetime.strptime(row[2], "%H:%M:%S").time() for row in history]


                df = pd.DataFrame({"Date": dates, "Time": times, "Water": values})
                agg = df.groupby("Date")["Water"].sum().reset_index()

                with col1:
                    st.line_chart(agg, x="Date", y="Water")

                with col2:
                    today = datetime.today().date()
                    last_7_days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

                    def hydration_emoji(amount):
                        if amount is None:
                            return ""   
                        elif amount < 500:
                            return "😟"   
                        elif amount < 1000:
                            return "🙂"   
                        else:
                            return "🟢" 

                    grid_emojis = []
                    for d in last_7_days:
                        day_data = agg[agg["Date"] == pd.to_datetime(d)]
                        amount = None if day_data.empty else day_data["Water"].iloc[0]
                        grid_emojis.append(hydration_emoji(amount))

                    st.subheader("Last 7 Days Hydration Status")

                    cols = st.columns(7)
                    for i, col in enumerate(cols):
                        day_str = last_7_days[i].strftime("%a")
                        col.markdown(
                            f"""
                            <div style="text-align:center;">
                                <div style="font-size:12px">{day_str}</div>
                                <div style="font-size:30px">{grid_emojis[i]}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

