## 2025-01-24 - [Semantic Streamlit Components & Sidebar Guidance]
**Learning:** Using semantic components like `st.title` and `st.caption` instead of custom HTML (`st.markdown`) improves accessibility for screen readers and ensures consistent styling. Providing a sidebar with "How to use" examples significantly improves discoverability for conversational agents with specialized tools.
**Action:** Always prefer semantic Streamlit components over custom HTML for headers and titles. Include a help sidebar or expander in agent-based UIs to guide user interactions.

## 2025-01-24 - [Immediate Feedback with st.status]
**Learning:** For long-running agent tasks, placing the agent call inside `st.status` within the `st.chat_message("assistant")` block provides immediate visual feedback that the app is working, preventing users from thinking the UI has frozen.
**Action:** Wrap blocking agent calls in `st.status` and ensure they are contextually placed within the chat bubble where the response will appear.
