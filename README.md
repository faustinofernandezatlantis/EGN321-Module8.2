# Capstone Report — From Workbook to Working Application

## Part 1 — What Was Inherited
- **Original Artifact:** Legacy Excel engineering workbook (`Engineering_Data_Workbook.xlsx`).
- **Designed Purpose:** Track sensor metrics and compute basic temperature and pressure averages manually.
- **Original Inputs:** Raw unvalidated decimal entries in Excel cells.
- **Original Outputs:** Unformatted static cells with total averages.
- **Identified Risks/Defects:**
  1. No input validation: Operators could enter negative absolute pressures or impossible temperatures (e.g., 9999°C).
  2. Silent failure: Excel computed formulas over blank or corrupted text cells without raising errors.
  3. Lack of unit standards: No enforcement of °C vs °F or kPa vs psi.
  4. No historical log: Previous calculations were overwritten manually without persistent recording.

## Part 2 — What Was Built
- **Core Technology:** Python 3.10+, Streamlit Web Dashboard, Pandas, SQLite 3, Pytest.
- **Key Modules Developed:**
  - Automated CSV parsing & schema validation.
  - Engineering safety refusal engine (-40°C to 120°C, 0 to 500 kPa).
  - Persistent execution log using SQLite (`data/history.db`).
  - Diagnostic logging system (`logs/app.log`).
  - Interactive multi-tab web dashboard with real-time metric cards and charts.

## Part 3 — Proving the Calculation
- **Test 1 (Known-Correct):** Excel workbook input `[25.0°C, 25.0°C]` verified against `test_1_known_correct_case()` producing exact output `25.0°C`.
- **Test 2 (Edge Case):** Boundary value `-40.0°C` tested and validated as minimum acceptable limit.
- **Test 3 (Invalid Input):** Sensor reading `155.0°C` triggers explicit system refusal.
- **Test 4 (Student-Created):** CSV missing required header `pressure` successfully caught and refused.

## Part 4 — Normal Operation Workflow
1. User activates `.venv` and runs `streamlit run app.py`.
2. User uploads `data/sample_input.csv`.
3. System validates column headers (`timestamp`, `temperature`, `pressure`).
4. System calculates metrics and updates green `HEALTHY` state banner.
5. System displays metrics, interactive line chart, appends record to SQLite DB, and logs event in `logs/app.log`.

## Part 5 — Refusal Logic & Engineering Safety
- **Condition:** Tool refuses files containing temperatures outside [-40.0°C, 120.0°C] or pressure outside [0.0, 500.0 kPa].
- **Why Refusing is Essential:** In safety-critical engineering systems, producing an erroneous number based on corrupted data can lead to hardware damage or misinformed decisions. Explicitly refusing execution forces operator intervention and protects physical equipment.

## Part 6 — System Evidence
- **Automated Testing:** 5 unit tests passing via `python -m pytest`.
- **SQLite History:** All execution outputs stored in `processing_history` table in `data/history.db`.
- **System Logs:** All operations written to timestamped `logs/app.log`.

## Part 7 — Failure and Recovery Demonstration
- **Controlled Failure:** Uploading a CSV file with out-of-range temperature data (`150°C`).
- **Detection:** App transitions status banner to `🔴 FAILED` and logs error entry in `app.log`.
- **Evidence:** SQLite records entry with status `FAILED_OUT_OF_BOUNDS`.
- **Recovery:** User uploads valid dataset `data/sample_input.csv`.
- **Verification:** App recovers status banner to `🟢 HEALTHY` and resumes normal operations.

## Part 8 — Silent Handoff Lessons Learned (Assignment 8.1 Summary)
- **Partner Struggle:** Partner confused how to launch app via CLI (`python app.py` vs `streamlit run app.py`).
- **Improvements Made:** Explicit launch instructions added to Quick Start in README; unit labels (°C, kPa) added directly to UI sidebar.
- **Key Lesson:** Software documentation must eliminate ambiguity for first-time operators.

## Part 9 — Key Assumptions
1. Temperature is recorded strictly in **Celsius (°C)**.
2. Pressure is recorded strictly in **Kilopascals (kPa)**.
3. Timestamps adhere to standard ISO/date formats.

## Part 10 — Known System Limitations
1. **Calibration:** System cannot verify whether physical sensors are calibrated accurately.
2. **File Types:** System accepts only standard UTF-8 encoded `.csv` files up to browser upload limits.

## Part 11 — AI Usage Transparency
- AI was used for UI boilerplate code, generating extended sample CSV data, and designing Pytest fixtures.
- All code, validations, and documentation were manually verified and executed. Details logged in `AI_LOG.md`.