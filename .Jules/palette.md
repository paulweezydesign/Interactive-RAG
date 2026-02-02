# Palette's Journal - Critical UX/Accessibility Learnings

## 2024-05-23 - Session Isolation in Streamlit
**Learning:** Using `@st.cache_resource` for an agent that maintains internal state (like chat history) causes state leakage across different user sessions.
**Action:** Always store session-specific objects (like agents with history) in `st.session_state` to ensure privacy and isolation.

## 2024-05-23 - Interactive Feedback in Streamlit
**Learning:** Blocking calls in Streamlit (like LLM generations) can make the UI feel frozen.
**Action:** Use `st.empty()` or `st.status()` placeholders to provide immediate visual feedback (e.g., "Thinking...") while the backend is processing.
