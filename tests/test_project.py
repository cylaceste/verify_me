import pytest
import sys
from pathlib import Path
current_script_path = Path(__file__).parent
parent_directory = current_script_path.parent
sys.path.insert(0, str(parent_directory))

from project import create_database, add_initial_users, run_airport_scenario
from verify_me_db.database import Database


@pytest.fixture
def test_database():
    db = create_database()
    add_initial_users(db)
    return db


def test_add_initial_users(test_database):
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


def test_create_tables(test_database):
    cursor = test_database.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    assert set(tables) == {('users',), ('cache',), ('images',)}


def test_add_entry(test_database):
    test_database.add_entry('users', (113, 'Test User', '2000-01-01', 'test@example.com', 103))
    cursor = test_database.conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = 113")
    entry = cursor.fetchone()
    assert entry == (113, 'Test User', '2000-01-01', 'test@example.com', 103)


def test_generate_verification(test_database):
    random_id_flight = test_database.generate_verification(111, 'Flight')
    random_id_bar = test_database.generate_verification(111, 'Bar')
    cursor = test_database.conn.cursor()
    cursor.execute("SELECT * FROM cache WHERE random_id = ?", (random_id_flight,))
    flight_entry = cursor.fetchone()
    cursor.execute("SELECT * FROM cache WHERE random_id = ?", (random_id_bar,))
    bar_entry = cursor.fetchone()
    assert flight_entry is not None and bar_entry is not None
    assert flight_entry[2] == 'Flight' and bar_entry[2] == 'Bar'


def test_get_verification(test_database):
    random_id_flight = test_database.generate_verification(111, 'Flight')
    verification_flight = test_database.get_verification(random_id_flight)
    assert verification_flight is not None
    assert verification_flight['name'] == 'Chieko'
    assert verification_flight['date_of_birth'] == '1234-05-06'


def test_non_existent_user(test_database):
    random_id_flight = test_database.generate_verification(111, 'Flight')
    with pytest.raises(FileNotFoundError):
        verification_flight = test_database.get_verification('000000')
