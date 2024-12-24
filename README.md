Overview
========

Welcome to Astronomer! This project was generated after you ran 'astro dev init' using the Astronomer CLI. This readme describes the contents of the project, as well as how to run Apache Airflow on your local machine.

Project Contents
================

# Weather ETL Pipeline using Apache Airflow

This project implements a **Weather ETL pipeline** using **Apache Airflow** to extract weather data from the **Open-Meteo API**, transform it, and load it into a **PostgreSQL** database.

The pipeline extracts weather data for multiple locations, processes it, and stores it in a PostgreSQL database for further analysis. This is a simple yet scalable ETL pipeline that can be used for weather-related data aggregation and analysis.

## Features

- **Extract**: Fetch current weather data for multiple locations from the **Open-Meteo API**.
- **Transform**: Process and structure the raw weather data into a format suitable for storage.
- **Load**: Insert the transformed data into a PostgreSQL database.

## Technologies Used

- **Apache Airflow**: For orchestrating the ETL process with scheduled tasks.
- **PostgreSQL**: To store the transformed weather data.
- **Open-Meteo API**: To fetch current weather data for specific latitude and longitude pairs.
- **Docker**: For running PostgreSQL in a containerized environment.

## Workflow

1. **Extract**: Using the `HttpHook` from Airflow to send a request to the Open-Meteo API for weather data for each location.
2. **Transform**: The raw data is then processed and transformed to extract only relevant fields like temperature, wind speed, and weather code.
3. **Load**: The transformed data is then inserted into a PostgreSQL database table. The table is created if it doesn't exist, and new records are added daily.

My Database after a some running of DAG
![Weather Image](weather_image.jpg)



For more [Refer to ETLWeather](https://github.com/krishnaik06/ETLWeather)
