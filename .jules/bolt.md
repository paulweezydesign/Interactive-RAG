## 2025-05-14 - [Performance optimization: Removing Selenium and Pandas]
**Learning:** Selenium and Pandas are heavy dependencies that significantly increase startup time and memory footprint. In a Streamlit RAG application, manual table formatting using `tabulate` and `html.escape` is much faster and safer than using Pandas for simple display tasks. Replacing Selenium with a search API (like SerpApi) reduces search latency from several seconds to milliseconds.
**Action:** Always prefer lightweight libraries like `tabulate` for table formatting and dedicated APIs for web search instead of headless browsers in performance-critical paths.

## 2025-05-14 - [Dependency conflict in Python 3.12]
**Learning:** Pydantic 2.2.1 has compatibility issues with Python 3.12 (specifically `ForwardRef._evaluate` missing `recursive_guard`). This can be resolved by upgrading LangChain to 0.2.0 and using the corresponding stable version pins.
**Action:** When working in Python 3.12, ensure LangChain and Pydantic versions are compatible to avoid runtime `TypeError`.
