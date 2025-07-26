import streamlit as st
from datetime import date
from db.database import init_db, insert_entry, get_entries_by_date
from agent.agent import process_inputs
import streamlit_authenticator as stauth

# ----------------------------
# ✅ Define User Credentials (Hardcoded)
# ----------------------------
credentials = {
    "usernames": {
        "fiza": {
            "name": "Fiza",
            "password": "fiza123"
        },
        "demo": {
            "name": "Demo User",
            "password": "demo"
        }
    }
}

# ----------------------------
# ✅ Initialize Authenticator
# ----------------------------
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="consciousday_cookie",
    key="secret_key_123",
    cookie_expiry_days=1
)

# ----------------------------
# ✅ Login Form
# ----------------------------
authenticator.login(location="main")

# ----------------------------
# ✅ Main App Logic
# ----------------------------
if st.session_state["authentication_status"]:
    st.set_page_config(page_title="ConsciousDay Agent", layout="centered")

    with st.sidebar:
        authenticator.logout(location="main", button_name="Logout")
        st.write(f"Welcome, *{st.session_state['name']}*")

    init_db()

    st.title("🌞 ConsciousDay Agent")
    st.header("📝 Morning Reflection Form")

    if st.button("🔄 Reset Reflection"):
        st.session_state.clear()
        st.rerun()


    # 🧠 Morning Form
    with st.form("morning_form"):
        journal = st.text_area("Morning Journal", height=150, placeholder="How are you feeling today?")
        dream = st.text_area("Dream", height=100, placeholder="Any dreams you remember?")
        intention = st.text_input("Intention of the Day", placeholder="What's your intention?")
        priorities = st.text_input("Top 3 Priorities (comma-separated)", placeholder="E.g. Focus, Hydrate, Workout")
        submitted = st.form_submit_button("✨ Generate Reflection")

    if submitted:
        if (
            "reflection_result" not in st.session_state or
            st.session_state.get("last_journal") != journal or
            st.session_state.get("last_dream") != dream or
            st.session_state.get("last_intention") != intention or
            st.session_state.get("last_priorities") != priorities
        ):
            with st.spinner("Thinking..."):
                reflection, strategy = process_inputs(journal, dream, intention, priorities)
                insert_entry(journal, intention, dream, priorities, reflection, strategy)

                st.session_state.reflection_result = (reflection, strategy)
                st.session_state.last_journal = journal
                st.session_state.last_dream = dream
                st.session_state.last_intention = intention
                st.session_state.last_priorities = priorities
        else:
            reflection, strategy = st.session_state.reflection_result

        st.success("🧠 Your Reflection & Strategy")
        st.subheader("🪞 Reflection Summary")
        parts = reflection.split("###")
        for part in parts:
            if part.strip():
                lines = part.strip().split("\n", 1)
                title = lines[0].strip()
                content = lines[1].strip() if len(lines) > 1 else ""
                with st.expander(f"🔹 {title}"):
                    st.markdown(content)

        st.subheader("📋 Suggested Day Strategy")
        st.markdown(strategy)

    # ----------------------------
    # 📅 View Past Entries
    # ----------------------------
    st.subheader("📅 View Past Entry")
    selected_date = st.date_input("Pick a date", value=date.today())

    if st.button("🔍 View Entry"):
        entries = get_entries_by_date(str(selected_date))
        if entries:
            for i, entry in enumerate(entries, start=1):
                (entry_id, entry_date, journal, intention, dream,
                 priorities, reflection, strategy) = entry

                st.success(f"📅 Entry {i} for {selected_date}")

                st.subheader("📝 Journal Entry")
                st.write(journal)

                st.subheader("💭 Dream Recall")
                st.write(dream)

                st.subheader("🎯 Daily Intention")
                st.write(intention)

                st.subheader("❗ Top Priorities")
                st.write(priorities)

                st.subheader("🧠 Reflection Insights")
                if reflection and "###" in reflection:
                    for section in reflection.split("###"):
                        if section.strip():
                            title, *content = section.strip().split("\n", 1)
                            with st.expander(title.strip()):
                                st.write(content[0] if content else "")
                else:
                    st.write(reflection)

                st.subheader("⏳ Daily Strategy")
                st.write(strategy)
                st.markdown("---")
        else:
            st.warning(f"No entry found for {selected_date}. Try creating an entry for today first.")

# ----------------------------
# 🚫 Invalid or No Login
# ----------------------------
elif st.session_state["authentication_status"] is False:
    st.error("❌ Incorrect username or password")
elif st.session_state["authentication_status"] is None:
    st.warning("👤 Please enter your username and password")
