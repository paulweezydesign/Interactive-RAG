## 2025-05-14 - Session isolation in Streamlit RAG apps
**Learning:** Using @st.cache_resource for a RAG agent that maintains state (like messages) causes that state to be shared across all user sessions.
**Action:** Always store stateful agent instances in st.session_state to ensure privacy and session isolation, while using st.status to handle the UX of initialization.
