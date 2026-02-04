## 2025-05-15 - [Eliminated 18s startup overhead by removing Selenium]
**Learning:** Initializing a headless Chrome browser in the constructor of a class (like UserProxyAgent) causes a massive (~18s) delay every time the agent is instantiated. If this is done in a Streamlit app without careful caching, it destroys the user experience. Replacing Selenium with a direct API call (SerpApi) and removing the browser init eliminates this bottleneck entirely.
**Action:** Always prefer API-based search/scraping over Selenium. If Selenium is unavoidable, never initialize it in a constructor; use lazy initialization or a shared singleton.

## 2025-05-15 - [Dependency reduction as a performance win]
**Learning:** Large dependencies like Pandas (~72MB) and Selenium (~29MB) add significant overhead to environment setup, container size, and import time (~1.2s for Pandas). For simple tasks like formatting tables or fetching web results, lightweight alternatives like `tabulate` and `requests` or dedicated APIs are much more efficient.
**Action:** Audit `requirements.txt` for heavy dependencies that can be replaced by standard library or lightweight alternatives for simple use cases.
