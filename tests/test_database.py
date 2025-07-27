import os
import sys
import pytest

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import init_db, insert_entry, get_entries_by_date

TEST_DB = "test_reflections.db"

def setup_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    init_db(db_name=TEST_DB)

def teardown_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_insert_and_retrieve_entry():
    insert_entry(
        journal="Test journal entry",
        intention="Be calm",
        dream="Flying through sky",
        priorities="Focus, Learn, Hydrate",
        reflection="Reflected thoughts",
        strategy="Test strategy",
        db_name=TEST_DB
    )

    entries = get_entries_by_date(db_name=TEST_DB)
    assert len(entries) == 1
    assert entries[0][3] == "Be calm"
    assert entries[0][2] == "Test journal entry"
