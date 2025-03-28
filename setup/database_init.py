from sqlalchemy import text
from helper.sql_engine import get_engine

def create_database(connection):
    connection.execute(text('CREATE DATABASE IF NOT EXISTS ufo_sightings'))
    connection.execute(text('USE ufo_sightings'))
    print("Switched to 'ufo_sightings' database.")

def drop_existing_tables(connection):
    tables = ['subscribers', 'ufo_sightings', 'movies', 'countries', 'event_dates']
    for table in tables:
        connection.execute(text(f'DROP TABLE IF EXISTS {table}'))
    print("Dropped all tables from previous runs (if they existed).")

def create_event_dates_table(connection):
    connection.execute(text('''
        CREATE TABLE IF NOT EXISTS event_dates (
            date_id INT PRIMARY KEY,
            date VARCHAR(10),
            date_full DATE
        )
    '''))
    print("Table 'event_dates' created successfully (if it didn't already exist).")

def create_countries_table(connection):
    connection.execute(text('''
        CREATE TABLE IF NOT EXISTS countries (
            country_id INT PRIMARY KEY,
            country VARCHAR(255) NOT NULL,
            population BIGINT,
            country_short VARCHAR(20)
        )
    '''))
    print("Table 'countries' created successfully (if it didn't already exist).")

def create_movies_table(connection):
    connection.execute(text('''
        CREATE TABLE IF NOT EXISTS movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            date_added DATE,
            date_added_formatted DATE,
            type VARCHAR(20),
            release_year INT,
            ufo_theme BOOLEAN NOT NULL DEFAULT FALSE,
            date_id INT,
            FOREIGN KEY (date_id) REFERENCES event_dates(date_id) ON DELETE CASCADE
        )
    '''))
    print("Table 'movies' created successfully (if it didn't already exist).")

def create_ufo_sightings_table(connection):
    connection.execute(text('''
        CREATE TABLE IF NOT EXISTS ufo_sightings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country_id INT,
            state VARCHAR(50),
            city VARCHAR(250),
            date DATE,
            date_id INT,
            FOREIGN KEY (country_id) REFERENCES countries(country_id) ON DELETE CASCADE,
            FOREIGN KEY (date_id) REFERENCES event_dates(date_id) ON DELETE CASCADE
        )
    '''))
    print("Table 'ufo_sightings' created successfully (if it didn't already exist).")

def create_subscribers_table(connection):
    connection.execute(text('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            subscribers INT NOT NULL DEFAULT 0,
            country_id INT,
            FOREIGN KEY (country_id) REFERENCES countries(country_id) ON DELETE CASCADE
        )
    '''))
    print("Table 'subscribers' created successfully (if it didn't already exist).")

def create_indexes(connection):
    connection.execute(text('CREATE INDEX idx_country_id_ufo ON ufo_sightings (country_id)'))
    connection.execute(text('CREATE INDEX idx_country_id_subs ON subscribers (country_id)'))
    print("Indexes created successfully.")

def main():
    engine = get_engine()
    with engine.connect() as connection:
        create_database(connection)
        drop_existing_tables(connection)
        create_event_dates_table(connection)
        create_countries_table(connection)
        create_movies_table(connection)
        create_ufo_sightings_table(connection)
        create_subscribers_table(connection)
        create_indexes(connection)

if __name__ == "__main__":
    main()
