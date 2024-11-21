import pandas as pd
import matplotlib.pyplot as plt
import sys
from pymongo import MongoClient
import numpy as np
import os
from dotenv import load_dotenv

# MongoDB connection setup
# load_dotenv()
# cluster_uri = os.getenv("DB_CONNECTION")

cluster_uri = "mongodb+srv://newTechPi:ggE84XiHnMBjXr7@clusternewtech.h05cs.mongodb.net/?retryWrites=true&w=majority&appName=clusterNewTech"

try:
    client = MongoClient(cluster_uri)
    db = client['newTech']
    collectionReports = db['reports']
    collectionDoorSensor = db['doorSensorTest']
except ConnectionError as err:
    print(f"Error connecting to MongoDB: {err}", file=sys.stderr)
    sys.exit(1)

# Compare foot traffic and sales, averaged per hour across days with complete data in both collections
def compareFootTrafficSales():
    # Load data from MongoDB
    reports_data = list(db.reportsTest.find())
    doorSensor_data = list(db.doorSensorTest.find())

    # Convert the data to pandas DataFrames
    doorSensor_df = pd.DataFrame(doorSensor_data)
    reports_df = pd.DataFrame(reports_data)

    # Convert date columns to datetime format
    reports_df['Date'] = pd.to_datetime(reports_df['Date'], format='%m-%d-%Y %H:%M', errors='coerce')
    doorSensor_df['date'] = pd.to_datetime(doorSensor_df['fulldate'], errors='coerce')

    # Extract the hour and date for grouping, formatting dates to a common format
    doorSensor_df['hour'] = doorSensor_df['date'].dt.hour
    doorSensor_df['day'] = doorSensor_df['date'].dt.strftime('%Y-%m-%d')  # Format as YYYY-MM-DD
    reports_df['hour'] = reports_df['Date'].dt.hour
    reports_df['day'] = reports_df['Date'].dt.strftime('%Y-%m-%d')  # Format as YYYY-MM-DD

    # Filter hours between 8 AM and 6 PM
    doorSensor_df = doorSensor_df[(doorSensor_df['hour'] >= 8) & (doorSensor_df['hour'] <= 18)]
    reports_df = reports_df[(reports_df['hour'] >= 8) & (reports_df['hour'] <= 18)]

    # Remove duplicates based on 'Order Name'
    reports_df_unique = reports_df.drop_duplicates(subset='Order Name')

    # Get common days with data in both datasets
    common_days = set(doorSensor_df['day']).intersection(set(reports_df_unique['day']))

    # Filter data to only include rows from common days
    doorSensor_df = doorSensor_df[doorSensor_df['day'].isin(common_days)]
    reports_df_unique = reports_df_unique[reports_df_unique['day'].isin(common_days)]

    # Group by day and hour, then calculate the mean for each hour across all days
    doorSensor_hourly_avg = doorSensor_df.groupby(['day', 'hour']).size().groupby('hour').mean()
    reports_hourly_avg = reports_df_unique.groupby(['day', 'hour']).size().groupby('hour').mean()

    # Check if there is data to plot
    if doorSensor_hourly_avg.empty and reports_hourly_avg.empty:
        print("No data available to display the plot.")
        return

    # Array for hours between 8 AM and 6 PM
    all_hours = np.arange(8, 19)

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 6))


    # Plot traffic and invoices
    ax.bar(all_hours - 0.2, doorSensor_hourly_avg.reindex(all_hours, fill_value=0), width=0.4, label='Average Foot Traffic', color='#4156b4')
    ax.bar(all_hours + 0.2, reports_hourly_avg.reindex(all_hours, fill_value=0), width=0.4, label='Average Invoices', color='#c87499')


    # Add labels and title
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Average Count')
    ax.set_title('Average Hourly Traffic and Invoices (Store Open from 8 AM to 6 PM)')
    ax.set_xticks(all_hours)
    ax.set_xticklabels([f'{i}:00' for i in all_hours])
    ax.legend()

    # Add grid lines for readability
    ax.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

    # Display the plot
    plt.tight_layout()
    plt.show()

# Check usage
if len(sys.argv) != 1:
    print("Usage: python script.py")
    sys.exit(1)

compareFootTrafficSales()

'''
# compare oil production of two countries in a given year.
def compareFootTrafficSales():
    # Create a plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot traffic (doorSensor data) as a blue bar
    ax.bar(all_hours - 0.2, doorSensor_hourly.reindex(all_hours, fill_value=0), width=0.4, label='Traffic (doorSensor)', color='blue')

    # Plot invoices (reports data) as a green bar
    ax.bar(all_hours + 0.2, reports_hourly.reindex(all_hours, fill_value=0), width=0.4, label='Invoices (reports)', color='green')

    # Add labels and title
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Count')
    ax.set_title('Hourly Traffic and Invoices (Store Open from 8 AM to 6 PM)')
    ax.set_xticks(all_hours)
    ax.set_xticklabels([f'{i}:00' for i in all_hours])  # Show hour labels like 8:00, 9:00, ..., 18:00
    ax.legend()

    # Add grid lines for better readability
    ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.7, alpha=0.7)

    # Display the plot
    plt.tight_layout()

    # Show the plot
    plt.show()

# if args is missing or is wrong
if len(sys.argv) != 1:
    print("Usage: python script.py")
    sys.exit(1)

compareFootTrafficSales()

'''