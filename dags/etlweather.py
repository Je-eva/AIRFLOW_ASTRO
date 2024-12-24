from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import requests
import json

# List of latitude and longitude pairs
LOCATIONS = [
    ('51.5074', '-0.1278'),  # London
    ('40.7128', '-74.0060'), # New York City
    ('35.6762', '139.6503'), # Tokyo
    ('-33.8688', '151.2093') # Sydney
]

POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

# DAG
with DAG(dag_id='weather_etl_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dags:

    @task()
    def extract_weather_data(latitude, longitude):
        """Extract weather data from Open-Meteo API using Airflow Connection."""
        # Use HTTP Hook to get connection details from Airflow connection
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')

        endpoint = f'/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
        response = http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch weather data: {response.status_code}")

    @task()
    def transform_weather_data(weather_data, latitude, longitude):
        """Transform the extracted weather data."""
        current_weather = weather_data['current_weather']
        transformed_data = {
            'latitude': latitude,
            'longitude': longitude,
            'temperature': current_weather['temperature'],
            'windspeed': current_weather['windspeed'],
            'winddirection': current_weather['winddirection'],
            'weathercode': current_weather['weathercode']
        }
        return transformed_data

    @task()
    def load_weather_data(transformed_data):
        """Load transformed data into PostgreSQL."""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            winddirection FLOAT,
            weathercode INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Insert transformed data into the table
        cursor.execute("""
        INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode']
        ))

        conn.commit()
        cursor.close()

    # Loop through each location using list comprehension
    for lat, lon in LOCATIONS:
        weather_data = extract_weather_data(lat, lon)
        transformed_data = transform_weather_data(weather_data, lat, lon)
        load_weather_data(transformed_data)
