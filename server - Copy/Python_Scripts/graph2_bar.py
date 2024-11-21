import matplotlib.pyplot as plt
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
        return collectionReports
    except pymongo.errors.ConnectionFailure:
        print("Failed to connect to MongoDB. Please make sure MongoDB is running.")
        sys.exit(1)

def popularPaymentMethod(collectionReports):
    # Load data from MongoDB
    reports_data = list(collectionReports.find())

    # Convert the data to a pandas DataFrame
    reports_df = pd.DataFrame(reports_data)

    # Replace NaN or empty values in 'Payment Method' with 'Not available'
    reports_df['Payment Method'] = reports_df['Payment Method'].fillna('Not available')
    reports_df.loc[reports_df['Payment Method'] == '', 'Payment Method'] = 'Not available'

    # Modify the 'Payment Method' to handle commas
    def process_payment_method(payment_method):
        # Check if the payment method contains a comma
        if ',' in payment_method:
            return 'Multiple payment methods'  # Categorize as "Multiple payment methods"
        else:
            # Strip spaces, convert to title case, and replace underscores with spaces
            return payment_method.strip().title().replace('_', ' ')

    # Apply the process_payment_method function to each row in 'Payment Method'
    reports_df['Payment_Method'] = reports_df['Payment Method'].apply(process_payment_method)

    # Group by 'Payment_Method' and count occurrences
    payment_counts = reports_df['Payment_Method'].value_counts()

    # Check if there is data to plot
    if payment_counts.empty:
        print("No data available to display the plot.")
        return

    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 8))  # Set the size of the figure

    payment_counts.plot(kind='barh', ax=ax, color=plt.cm.Paired.colors[:len(payment_counts)])

    # Set the title and labels
    ax.set_title('Most Popular Payment Methods')
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Payment Method')

    # Rotate the labels on the y-axis for better readability
    plt.yticks(rotation=0)

    # Display the plot
    plt.tight_layout()

    filename = 'graph2.png'

    plt.savefig(filename)
    print(filename)

def main():
    try:
        collectionReports = connect_mongodb()
        popularPaymentMethod(collectionReports)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    load_dotenv()  # take environment variables from .env.
    main()
