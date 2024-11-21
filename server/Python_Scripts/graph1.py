import matplotlib.pyplot as plt
import numpy as np
import pymongo
import pandas as pd
import sys
import os
from dotenv import load_dotenv

def connect_mongodb():
    """Connect to MongoDB."""
    try:
        client = pymongo.MongoClient(os.getenv('DATABASE_CONNECTION_STRING'))
        db = client['newTech']
        collectionReports = db['reports']
        collectionDoorSensor = db['doorSensor']
        return collectionReports, collectionDoorSensor
    except pymongo.errors.ConnectionFailure:
        print("Failed to connect to MongoDB. Please make sure MongoDB is running.")
        sys.exit(1)

def compareFootTrafficSales(collectionReports, collectionDoorSensor):
    # Load data from MongoDB
    reports_data = list(collectionReports.find())
    doorSensor_data = list(collectionDoorSensor.find())

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

    # Apply the transformation: divide by 2 because people open the door twice
    doorSensor_hourly_avg = (doorSensor_hourly_avg / 2)

    reports_hourly_avg = reports_df_unique.groupby(['day', 'hour']).size().groupby('hour').mean()

    # Check if there is data to plot
    if doorSensor_hourly_avg.empty and reports_hourly_avg.empty:
        print("No data available to display the plot.")
        return

    # Array for hours between 8 AM and 6 PM
    all_hours = np.arange(8, 19)

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))

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

    filename = 'graph1.png'

    plt.savefig(filename)
    print(filename)

def main():
    """Main function."""
    try:
        collectionReports, collectionDoorSensor = connect_mongodb()
        compareFootTrafficSales(collectionReports, collectionDoorSensor)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    load_dotenv()  # take environment variables from .env.
    main()