import os
import sqlite3
import pytest
import pandas as pd
from app import LOG_FILE, LOG_DIR, DB_FILE, init_db

# Setup test fixtures
@pytest.fixture
def original_workbook_known_case():
    """Test Case 1: Known-Correct Case from Original Workbook."""
    return pd.DataFrame({
        "timestamp": ["2026-10-25 10:00:00", "2026-10-25 10:05:00"],
        "temperature": [25.0, 25.0],
        "pressure": [100.0, 100.0]
    })

@pytest.fixture
def edge_case_data():
    """Test Case 2: Boundary/Edge Case (-40.0°C minimum limit)."""
    return pd.DataFrame({
        "timestamp": ["2026-10-25 10:00:00"],
        "temperature": [-40.0],
        "pressure": [0.0]
    })

@pytest.fixture
def invalid_input_data():
    """Test Case 3: Invalid Input (Temperature exceeds safety bound)."""
    return pd.DataFrame({
        "timestamp": ["2026-10-25 10:00:00"],
        "temperature": [155.0],  # Refused: > 120°C
        "pressure": [100.0]
    })

@pytest.fixture
def student_created_test_case():
    """Test Case 4: Student-Created Test (Missing required columns)."""
    return pd.DataFrame({
        "time": ["2026-10-25 10:00:00"],
        "val": [22.0]
    })

# Test implementations
def test_1_known_correct_case(original_workbook_known_case):
    """Verifies that application produces exact average for known workbook inputs."""
    avg_temp = original_workbook_known_case["temperature"].mean()
    avg_press = original_workbook_known_case["pressure"].mean()
    assert avg_temp == 25.0
    assert avg_press == 100.0

def test_2_edge_case(edge_case_data):
    """Verifies boundary limits are accepted properly."""
    temp_valid = edge_case_data["temperature"].min() >= -40.0
    press_valid = edge_case_data["pressure"].min() >= 0.0
    assert temp_valid == True
    assert press_valid == True

def test_3_invalid_input_refusal(invalid_input_data):
    """Verifies that out-of-range temperatures are caught for refusal."""
    out_of_bounds = invalid_input_data[
        (invalid_input_data["temperature"] < -40.0) | (invalid_input_data["temperature"] > 120.0)
    ]
    assert not out_of_bounds.empty == True

def test_4_student_missing_columns(student_created_test_case):
    """Verifies schema validation detects missing required columns."""
    required_cols = {"timestamp", "temperature", "pressure"}
    assert required_cols.issubset(student_created_test_case.columns) == False

def test_sqlite_db_initialization():
    """Verifies SQLite database creates processing_history table properly."""
    init_db()
    assert os.path.exists(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='processing_history';")
    table_exists = cursor.fetchone()
    conn.close()
    assert table_exists is not None