import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from dotenv import load_dotenv

def connect_mongodb():
    """Connect to MongoDB."""
    try:
        client = pymongo.MongoClient(os.getenv('DATABASE_CONNECTION_STRING'))
        db = client['newTech']
        collectionReports = db['reports']
        return collectionReports
    except pymongo.errors.ConnectionFailure:
        print("Failed to connect to MongoDB. Please make sure MongoDB is running.")
        sys.exit(1)

def averageOrderedQuantityPerDay(collectionReports):
    # Load data from MongoDB
    reports_data = list(collectionReports.find())
    
    if not reports_data:  # Check if there's no data
        print("no_data.png")
    else:
        # Convert the data to a pandas DataFrame
        reports_df = pd.DataFrame(reports_data)

        # Replace missing or empty 'Ordered Quantity' values with 0 and ensure it's an integer type
        reports_df['Ordered Quantity'] = reports_df['Ordered Quantity'].fillna(0).astype(int)

        # Convert 'Date' column to datetime format
        reports_df['Date'] = pd.to_datetime(reports_df['Date'], format='%m-%d-%Y %H:%M', errors='coerce')

        # Remove time component from the date to group by date only
        reports_df['Date'] = reports_df['Date'].dt.date

        # Group by 'Date' to calculate the total ordered quantity and number of orders per day
        daily_order_totals = reports_df.groupby('Date')['Ordered Quantity'].sum()
        daily_order_counts = reports_df.groupby('Date')['Order Name'].nunique()

        # Calculate the average ordered quantity per order per day
        avg_ordered_quantity_per_day = daily_order_totals / daily_order_counts

        # Check if there is data to plot
        if avg_ordered_quantity_per_day.empty:
            print("No data available to calculate the average ordered quantity per day.")
            return

        # Sort by date and keep the 7 most recent dates
        avg_ordered_quantity_per_day = avg_ordered_quantity_per_day.sort_index(ascending=False).head(7)

        # Sort back to chronological order for plotting
        avg_ordered_quantity_per_day = avg_ordered_quantity_per_day.sort_index()

        # Define the custom color order
        colors = ['#4156b4', '#7248b0', '#98319f', '#b50084', '#c40061', '#ca003b', '#c60606']

        # Create a bar chart for the average ordered quantity per day
        fig, ax = plt.subplots(figsize=(10, 6))
        avg_ordered_quantity_per_day.plot(kind='bar', color=colors, ax=ax)

        # Add labels and title
        ax.set_xlabel('Date')
        ax.set_ylabel('Average Ordered Quantity')
        ax.set_title('Average Ordered Quantity Per Order per Day')

        # Format the x-axis to show the dates properly
        ax.set_xticklabels([str(date) for date in avg_ordered_quantity_per_day.index], rotation=45, ha='right')
        
        # Add a grid for better readability
        ax.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

        # Get the current y-tick positions
        yticks = ax.get_yticks()

        # Loop through the y-tick positions and make the integer ones bold
        for tick in yticks:
            if tick.is_integer():  # Check if it's an integer
                ax.axhline(y=tick, color='black', linewidth=2, linestyle=':')  # Bold grid line for integers

        # Display the plot
        plt.tight_layout()

        filename = 'graph4.png'
        plt.savefig(filename)
        print(filename)

def main():
    try:
        collectionReports = connect_mongodb()
        averageOrderedQuantityPerDay(collectionReports)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    load_dotenv()  # take environment variables from .env.
    main()
