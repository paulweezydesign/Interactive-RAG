## 2025-02-01 - [Startup Optimization]
**Learning:** Selenium WebDriver initialization in the agent's `__init__` method was adding 2-5 seconds of latency to the first user interaction, even if no web search was performed. Additionally, importing large libraries like Pandas added ~0.6s of overhead.
**Action:** Use lazy initialization for heavy resources like browsers and prefer lightweight alternatives (e.g., tabulate) over heavy ones (e.g., Pandas) for simple tasks like table formatting.
