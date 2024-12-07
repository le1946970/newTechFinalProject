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

def popularBarcodes(collectionReports, top_n=1):
    # Load data from MongoDB
    reports_data = list(collectionReports.find())
    
    if not reports_data:  # Check if there's no data
        print("no_data.png")
    else:
        # Convert the data to a pandas DataFrame
        reports_df = pd.DataFrame(reports_data)

        # Drop rows where 'Barcode' or 'Date' is missing
        reports_df = reports_df[~reports_df['Barcode'].isna() & (reports_df['Barcode'] != '')]
        reports_df = reports_df[~reports_df['Date'].isna()]

        # Replace missing 'Ordered Quantity' values with 0 and ensure it's an integer type
        reports_df['Ordered Quantity'] = reports_df['Ordered Quantity'].fillna(0).astype(int)

        # Ensure 'Date' is in datetime format
        reports_df['Date'] = pd.to_datetime(reports_df['Date'])

        # Add a column for the day of the week
        reports_df['DayOfWeek'] = reports_df['Date'].dt.day_name()

        # Group by 'DayOfWeek' and 'Barcode', then calculate the total ordered quantity for each barcode per day
        daily_barcode_counts = reports_df.groupby(['DayOfWeek', 'Barcode'])['Ordered Quantity'].sum().reset_index()

        # Find the most popular barcode per day
        daily_top_barcodes = daily_barcode_counts.loc[daily_barcode_counts.groupby('DayOfWeek')['Ordered Quantity'].idxmax()]

        # Sort the data by day of the week in the correct order (Monday, Tuesday, etc.)
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_top_barcodes['DayOfWeek'] = pd.Categorical(daily_top_barcodes['DayOfWeek'], categories=days_order, ordered=True)
        daily_top_barcodes = daily_top_barcodes.sort_values('DayOfWeek')

        # Check if there is data to plot
        if daily_top_barcodes.empty:
            print("No data available to display the plot.")
            return

        # Define a list of colors for each day of the week
        colors = [
            '#4156b4', '#634db2', '#7f41ab', '#98319f', '#ad178e', 
            '#bd0079', '#c40061'
        ]

        # Create bar chart showing the most popular barcode for each day of the week
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(daily_top_barcodes['DayOfWeek'], daily_top_barcodes['Ordered Quantity'], color=colors[:len(daily_top_barcodes)])

        # Add labels and title
        ax.set_ylabel('Ordered Quantity')
        ax.set_title(f'Most Popular Barcode by Day of the Week')

        # Display the ordered barcode for each day, positioning the text inside or below the bar
        for i, row in daily_top_barcodes.iterrows():
            # If the quantity is large, place the text inside the bar, otherwise below the bar
            if row['Ordered Quantity'] > 20:
                ax.text(row['DayOfWeek'], row['Ordered Quantity'] / 2, f"{row['Barcode']}", ha='center', va='center', color='white', fontsize=10, rotation=90)
            else:
                ax.text(row['DayOfWeek'], row['Ordered Quantity'] + 1, f"{row['Barcode']}", ha='center', va='bottom', fontsize=10)

        # Add grid
        ax.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7)

        # Display the plot
        plt.tight_layout()

        filename = 'graph3.png'

        plt.savefig(filename)
        print(filename)

def main():
    try:
        collectionReports = connect_mongodb()
        popularBarcodes(collectionReports)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    load_dotenv()  # take environment variables from .env.
    main()
