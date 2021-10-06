#!/usr/bin/env python
# coding: utf-8

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import date
from datetime import timedelta


# Read the .env file
load_dotenv()

appId = os.getenv("appId")
appKey = os.getenv("appKey")

# Get list of airport
my_airport_df = pd.read_csv("my_airport.csv")
airport_icao = my_airport_df["icao"].tolist()
airport_iata = my_airport_df["iata"].tolist()

# Get today's date 
today = date.today()

# Get tomorrow's date
tomorrow = today + timedelta(days=1)

# Separate date into ymd
year = tomorrow.year
month = tomorrow.month
day = tomorrow.day

# Initialize list to store number of landing flights
total_landing_flights = []
flights_num = 0

# Iterate over all airport
for code in airport_icao:
    arrivalAirportCode = code
    
    # Iterate over 0 to 23 hour
    for hour in range(24):
        hourOfDay = hour
         
        try:
            response = requests.get(f"https://api.flightstats.com/flex/schedules/rest/v1/json/to/{arrivalAirportCode}/arriving/{year}/{month}/{day}/{hourOfDay}?appId={appId}&appKey={appKey}")
            flights_num += len(response.json()["scheduledFlights"])
        
        # Catch KeyError due to unavailble airport ICAO code in the database
        except KeyError:
            index = airport_icao.index(code)
            arrivalAirportCode = airport_iata[index]
            
            # Assign null to flights_num if alternative code (IATA) is missing
            if pd.isna(arrivalAirportCode):
                flights_num = float("nan")
                break
            
            else:
                response = requests.get(f"https://api.flightstats.com/flex/schedules/rest/v1/json/to/{arrivalAirportCode}/arriving/{year}/{month}/{day}/{hourOfDay}?appId={appId}&appKey={appKey}")
                flights_num += len(response.json()["scheduledFlights"])
    
    total_landing_flights.append(flights_num)
    flights_num = 0

# Store results in a new column
my_airport_df["total_landing_flights"] = total_landing_flights

# Sort df by total_landing_flights
my_airport_df.sort_values(by="total_landing_flights", ascending=False, inplace=True)

# Add date column for queried date
my_airport_df["date"] = tomorrow.isoformat()

# Export df to csv
my_airport_df.to_csv("my_airport_traffic.csv", index=False)