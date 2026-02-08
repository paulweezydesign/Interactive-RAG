## 2025-05-22 - [Extreme startup delay from Selenium]
**Learning:** Initializing a Selenium WebDriver in a class constructor causes a massive (~18s) delay in application startup. This is especially problematic in Streamlit apps where user perception of speed is critical.
**Action:** Replace browser-based automation with API-based alternatives (like SerpApi) whenever possible. If browser automation is necessary, use lazy initialization.

## 2025-05-22 - [Pandas overhead for simple formatting]
**Learning:** Importing Pandas adds ~0.7s to 1.2s overhead. Using it just for Markdown/HTML table conversion is inefficient.
**Action:** Use lighter alternatives like `tabulate` or native string formatting for simple data display.

## 2025-05-22 - [LangChain 0.2.0 and Python 3.12 compatibility]
**Learning:** Old versions of LangChain and Pydantic (v1 bridge) are broken on Python 3.12 due to a change in `ForwardRef._evaluate`. A major version jump to LangChain 0.2.0 is often required to resolve this in a Python 3.12 environment.
**Action:** When working with LangChain in Python 3.12, prefer modern versions (0.2.0+) and updated import paths (`langchain_community`, `langchain_text_splitters`).
