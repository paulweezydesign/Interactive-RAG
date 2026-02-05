## 2024-05-23 - [Semantic Headers and Layout]
**Learning:** Using semantic Streamlit components like `st.title` and `st.divider` instead of raw HTML/Markdown improves accessibility for screen readers and ensures consistent styling with the Streamlit theme.
**Action:** Always prefer `st.title`, `st.header`, and `st.divider` over custom HTML `<span>` or `----` markdown.

## 2024-05-23 - [Visual Feedback for Blocking Calls]
**Learning:** For long-running agent calls, `st.status` provides a much better UX than a simple spinner, as it can be expanded to show sub-steps of the process (like searching or reading URLs).
**Action:** Wrap complex agent calls in `st.status("Thinking...")` to keep users informed.
