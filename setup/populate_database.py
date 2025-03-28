# Import functions from data_cleaning_functions.py
from data_cleaning_functions import create_countries, clean_movies_data, clean_ufo_reports, clean_subscriber_data, create_date_index
import pandas as pd
from helper.sql_engine import get_engine 

# Get the engine
engine = get_engine()

# Use the functions
if __name__ == "__main__":
    # Create countries DataFrame
    population_df = pd.read_csv(r"C:\Users\Martijn\Downloads\population_date.csv")
    countries_df = create_countries(population_df)
    
    # Clean movies data
    movies_df = pd.read_csv(r"C:\Users\Martijn\Downloads\netflix_titles_anandshaw.csv") 
    cleaned_movies_df = clean_movies_data(movies_df)
    
    # Clean UFO reports data
    ufo_report_df = pd.read_csv(r"C:\Users\Martijn\Downloads\nuforc_reports (1).csv")
    cleaned_ufo_df = clean_ufo_reports(ufo_report_df, countries_df)
    
    # Clean subscribers data
    subscribers_df = pd.read_csv(r"C:\Users\Martijn\Downloads\subscribers_netflix_2024 (1).csv")
    final_subscribers_df = clean_subscriber_data(subscribers_df, countries_df)

    # Create events dates df
    final_ufo_report_df, final_movies_df, date_index_df = create_date_index(cleaned_ufo_df, cleaned_movies_df)


    with engine.connect() as connection:
        # Load event_dates DataFrame into the database
        date_index_df.columns = ['date', 'date_id', "date_full"]  # Rename columns to match SQL table
        date_index_df.to_sql('event_dates', schema="ufo_sightings", con=connection, if_exists='append', index=False)
        
        # Load countries DataFrame into the database
        countries_df.columns = ['country_id', "country_short", 'country', 'population']  # Rename columns to match SQL table
        countries_df.to_sql('countries', schema="ufo_sightings", con=engine, if_exists='append', index=False)

        # Load movies DataFrame into the database
        final_movies_df.to_sql('movies', con=connection, schema="ufo_sightings", if_exists='append', index=False)
        
        # Load UFO sightings DataFrame into the database
        final_ufo_report_df.to_sql('ufo_sightings', con=connection, schema="ufo_sightings", if_exists='append', index=False)

        # Load subscribers DataFrame into the database
        final_subscribers_df.to_sql('subscribers', con=connection, schema="ufo_sightings", if_exists='append', index=False)