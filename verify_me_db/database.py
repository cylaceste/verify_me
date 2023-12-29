import sqlite3
import random
import string
from .service_info import get_model_for_service
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE users (
                            user_id INTEGER PRIMARY KEY,
                            name TEXT,
                            date_of_birth TEXT,
                            email TEXT,
                            image_id INTEGER)''')

        cursor.execute('''CREATE TABLE cache (
                            cache_id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            service_type TEXT,
                            expiration DATETIME,
                            random_id TEXT)''')

        cursor.execute('''CREATE TABLE images (
                            image_id INTEGER PRIMARY KEY,
                            image_url TEXT)''')

        self.conn.commit()

    def add_entry(self, table, data):
        cursor = self.conn.cursor()
        placeholders = ', '.join(['?'] * len(data))
        query = f'INSERT INTO {table} VALUES ({placeholders})'
        cursor.execute(query, data)
        self.conn.commit()

    def generate_verification(self, user_id, service_type):
        random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        expiration = datetime.now() + timedelta(minutes=5)  # Set expiration to 5 minutes from now
        formatted_expiration = expiration.strftime('%Y-%m-%d %H:%M:%S')
        self.add_entry('cache', (None, user_id, service_type, formatted_expiration, random_id))
        return random_id


    def get_verification(self, random_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT u.name, u.date_of_birth, i.image_url, c.service_type
                          FROM cache c
                          JOIN users u ON c.user_id = u.user_id
                          JOIN images i ON u.image_id = i.image_id
                          WHERE c.random_id = ?''', (random_id,))
        result = cursor.fetchone()

        if not result:
            raise FileNotFoundError("Could not find corresponding information for this person. "
                                    "Please ask them to generate a new one.")

        if result:
            data = {
                "name": result[0],
                "date_of_birth": result[1],
                "image_url": result[2]
            }
            service_type = result[3]
            model = get_model_for_service(service_type, data)
            return model
        return None


def main():
    db = Database()
    db.initialize_entries()
    random_id = db.generate_verification(1, 'Flight', '2023-12-31 23:59:59')
    verification_info = db.get_verification(random_id)
    print(verification_info)

if __name__ == "__main__":
    main()
