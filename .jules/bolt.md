## 2025-01-24 - [Optimizing Resource Usage and Ingestion Speed]
**Learning:** Replacing heavy dependencies like `pandas` and `Playwright` with lighter alternatives (`tabulate`, `requests`) can significantly improve startup time and memory footprint. However, manual HTML generation (replacing `pandas.to_html()`) introduces XSS risks if content is not properly escaped.
**Action:** Always use `html.escape()` when manually building HTML strings from user-provided or dynamic data. Use lazy-loading for heavy initializations (like Selenium) to avoid overhead in code paths that don't require them.
