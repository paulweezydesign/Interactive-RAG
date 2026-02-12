## 2026-02-06 - Streamlit Chat UX Improvements
**Learning:** Wrapping blocking agent calls with `st.status` inside the `st.chat_message` block significantly improves perceived performance by giving the user immediate visual feedback ("Thinking...") before the response starts streaming or appearing.
**Action:** Always prefer `st.status` for long-running agent tasks in Streamlit chat interfaces.

**Learning:** Essential session controls like "Clear Chat History" should be easily accessible in a sidebar rather than requiring natural language commands, providing a faster and more reliable "escape hatch" for the user.
**Action:** Include common session management tools in a sidebar for chat-based applications.
