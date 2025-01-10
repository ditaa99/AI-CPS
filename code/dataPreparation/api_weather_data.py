'''we already have completed the scraping puzzle piece, but we wanted this extra data
the data is already cleaned, hence it is straight saved in /cleaned folder'''

import os
import pandas as pd
from datetime import datetime
from meteostat import Point, Hourly

# Set time period, we want to analyze the year 2024
start = datetime(2024, 1, 1)
end = datetime(2024, 12, 31)

# Create Points for Berlin and Potsdam
berlin = Point(52.5200, 13.4050, 34)  # Berlin
potsdam = Point(52.3989, 13.0657, 34)  # Potsdam

# Get hourly data for Berlin and Potsdam
data_berlin = Hourly(berlin, start, end).fetch()
data_potsdam = Hourly(potsdam, start, end).fetch()

# Add location columns
data_berlin['Location'] = 'Berlin'
data_potsdam['Location'] = 'Potsdam'

# Combine data into a single DataFrame
data = pd.concat([data_berlin[['prcp', 'wspd', 'wdir', 'Location']], data_potsdam[['prcp', 'wspd', 'wdir', 'Location']]], axis=0)
data.columns = ['Precipitation', 'Wind Speed', 'Wind Direction', 'Location']

# Filter data to only include times when it rained (precipitation > 0)
rain_data = data[data['Precipitation'] > 0]

# Find start and end times of rain occurrences with locations
rain_occurrences = []
start_time = None
current_location = None

for i in range(len(rain_data)):
    if start_time is None:
        start_time = rain_data.index[i]
        current_location = rain_data['Location'][i]
    if (i == len(rain_data) - 1 or (rain_data.index[i + 1] - rain_data.index[i]) > pd.Timedelta(hours=1) or rain_data['Location'][i + 1] != current_location):
        end_time = rain_data.index[i]
        rain_occurrences.append([start_time, end_time, rain_data['Precipitation'][i], rain_data['Wind Speed'][i], rain_data['Wind Direction'][i], current_location])
        start_time = None

# Create DataFrame for rain occurrences in Ber and Pdm and sort it chronologically
rain_occurrences_df = pd.DataFrame(rain_occurrences, columns=['Start Time', 'End Time', 'Precipitation', 'Wind Speed', 'Wind Direction', 'Location'])
rain_occurrences_df = rain_occurrences_df.sort_values(by='Start Time')

# Save data
os.makedirs('data/cleaned', exist_ok=True)
rain_occurrences_df.to_csv('data/cleaned/weather_data_2024.csv', index=False)

#Commented out after the first run
# print("Rain occurrences with locations saved to 'data/weather_data_2024.csv':")
# print(rain_occurrences_df)
