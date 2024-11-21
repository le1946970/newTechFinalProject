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

def popularBarcodes(collectionReports, top_n=10):
    # Load data from MongoDB
    reports_data = list(collectionReports.find())

    # Convert the data to a pandas DataFrame
    reports_df = pd.DataFrame(reports_data)

    # Replace missing or empty 'Barcode' values with 'Not available'
    reports_df['Barcode'] = reports_df['Barcode'].fillna('Not available')
    reports_df.loc[reports_df['Barcode'] == '', 'Barcode'] = 'Not available'

    # Replace missing 'Ordered Quantity' values with 0 and ensure it's an integer type
    reports_df['Ordered Quantity'] = reports_df['Ordered Quantity'].fillna(0).astype(int)

    # Group by 'Barcode' and sum 'Ordered Quantity' for each
    barcode_counts = reports_df.groupby('Barcode')['Ordered Quantity'].sum().sort_values(ascending=False).head(top_n)

    # Check if there is data to plot
    if barcode_counts.empty:
        print("No data available to display the plot.")
        return

    # Define a list of colors (hex codes) for each barcode
    colors = [
        '#4156b4', '#634db2', '#7f41ab', '#98319f', '#ad178e', 
        '#bd0079', '#c40061', '#c90048', '#cc002c', '#c60606'
    ]

    # Create bar chart with each barcode having a different color
    fig, ax = plt.subplots(figsize=(10, 6))
    barcode_counts.plot(kind='bar', color=colors[:len(barcode_counts)], ax=ax)

    # Add labels and title
    ax.set_xlabel('Barcode')
    ax.set_ylabel('Total Ordered Quantity')
    ax.set_title(f'Top {top_n} Most Popular Barcodes by Ordered Quantity')

    # Rotate x-axis labels for readability
    ax.set_xticklabels(barcode_counts.index, rotation=45, ha='right')

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
