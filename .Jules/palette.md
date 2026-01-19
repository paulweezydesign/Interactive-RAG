## 2024-05-20 - Streamlit UI Rendering Dependencies

**Learning:** The Streamlit UI may not render completely (e.g., chat input missing) if the required API keys in `rag/params.py` are not provided. This blocks frontend verification.

**Action:** When working on frontend changes, ensure that either valid API keys are available or the code is temporarily modified to render the UI without them. Otherwise, frontend verification will not be possible.
