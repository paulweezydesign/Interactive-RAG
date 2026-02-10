## 2024-05-23 - [Streamlit Session Isolation]
**Learning:** Using `@st.cache_resource` for agents that hold state (like message history) creates a singleton shared across all users. For session isolation, store the agent in `st.session_state`.
**Action:** Use `st.session_state` for stateful agents in multi-user Streamlit apps.

## 2024-05-23 - [Immediate Feedback in Chat]
**Learning:** Moving a blocking agent call inside the `with st.chat_message("assistant")` block allows displaying a placeholder (like "Thinking...") immediately, improving perceived performance.
**Action:** Always wrap blocking backend calls with a UI feedback indicator within the target message container.
