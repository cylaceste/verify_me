import pytest
import sys
from pathlib import Path
from unittest.mock import patch
current_script_path = Path(__file__).parent
parent_directory = current_script_path.parent
sys.path.insert(0, str(parent_directory))
from datetime import datetime

from project import create_database, add_initial_users, run_airport_scenario
from verify_me_db.database import Database


@pytest.fixture
def test_database():
    db = create_database()
    add_initial_users(db)
    return db


def test_add_initial_users_worked(test_database):
    cursor = test_database.conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    assert len(users) == 2  # Two users added
    assert users[0][1] == 'Chieko'  # I'm the first user


def test_run_airport_scenario(test_database, capsys):
    run_airport_scenario(test_database)
    captured = capsys.readouterr()
    assert "Cool beans, the photo matches" in captured.out
    assert "drinking age" in captured.out


def test_get_verification(test_database):
    random_id_flight = test_database.generate_verification(111, 'Flight')
    verification_flight = test_database.get_verification(random_id_flight)
    assert verification_flight is not None
    assert verification_flight['name'] == 'Chieko'
    assert verification_flight['date_of_birth'] == '1234-05-06'


def test_non_existent_user(test_database):
    with pytest.raises(FileNotFoundError):
        test_database.get_verification('000000')
