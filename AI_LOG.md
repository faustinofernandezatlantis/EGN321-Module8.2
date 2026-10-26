\# AI Usage Log (`AI\_LOG.md`) — Capstone Project



\## 1. Overview \& Compliance

This document records the usage of Artificial Intelligence (AI) tools during the development of the \*\*Capstone Application: From Workbook to Working Application\*\* (EGN-321 Assignment 8.2). 



In accordance with course guidelines, AI tools were utilized during the preparation and development phase for boilerplate code generation, test case structures, and extended dataset creation. AI tools \*\*will not\*\* be used during the live code challenge or technical defense.



\---



\## 2. AI Tools Utilized

\- \*\*AI Models:\*\* OpenAI ChatGPT / Claude / Gemini

\- \*\*Scope of Use:\*\*

&#x20; - Refactoring the Streamlit application to integrate SQLite history tracking and diagnostic logging.

&#x20; - Generating Pytest fixtures for original workbook verification cases.

&#x20; - Generating an extended 100-record engineering sample dataset.

&#x20; - Structuring the Capstone report and slide deck outline.



\---



\## 3. Prompts, Outputs, and Verification



\### Prompt 1: SQLite History Integration \& Multi-Tab UI

\- \*\*Task:\*\* Refactor `app.py` to add persistent SQLite history recording for every executed calculation and display execution history in a dedicated UI tab.

\- \*\*AI Contribution:\*\* Provided the `init\_db()` and `save\_to\_history()` function implementations along with `st.tabs()` structure.

\- \*\*Verification \& Modifications:\*\* Manually tested database operations to ensure `history.db` was created inside the `data/` directory and correctly recorded states (`HEALTHY`, `FAILED\_OUT\_OF\_BOUNDS`, `FAILED\_MISSING\_COLUMNS`).



\### Prompt 2: Original Workbook Pytest Suite

\- \*\*Task:\*\* Create `test\_app.py` test cases reflecting the four required test categories (Known-Correct Workbook Case, Edge/Boundary Case, Invalid Input Refusal, and Student-Created Missing Header Case).

\- \*\*AI Contribution:\*\* Generated the initial Pytest code structure and assertion statements.

\- \*\*Verification \& Modifications:\*\* Executed `python -m pytest` locally, verified all 5 tests passed, and confirmed database table creation test logic.



\### Prompt 3: Extended Engineering Dataset

\- \*\*Task:\*\* Generate a 100-row CSV file containing realistic time-series temperature and pressure readings within safe operating limits.

\- \*\*AI Contribution:\*\* Produced `data/sample\_input.csv` with 5-minute time increments and safe engineering values.

\- \*\*Verification \& Modifications:\*\* Imported the file into the Streamlit app to confirm that summary metrics and line charts rendered without formatting issues.



\---



\## 4. Statement of Responsibility

All AI-generated code, tests, database interactions, and documentation were manually reviewed, executed, and verified by the student. The final working system, logic integrity, and ability to defend the codebase during the live challenge remain the sole responsibility of the student.

