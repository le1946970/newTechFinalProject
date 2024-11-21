import matplotlib.pyplot as plt
import pymongo
import pandas as pd
import sys
import os
import numpy as np
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
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, texts, autotexts = ax.pie(payment_counts, colors=plt.cm.Paired.colors, autopct='%1.1f%%', startangle=180, wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'}, pctdistance=0.85)

    # Add annotations
    labels=payment_counts.index
    for i, (wedge, label) in enumerate(zip(wedges, labels)):
        ang = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))

        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"

        ax.annotate(label, xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment,
                    arrowprops=dict(arrowstyle="-", connectionstyle=connectionstyle))


    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
 
    # Adding Circle in Pie chart
    fig.gca().add_artist(centre_circle)

    ax.set_title('Most Popular Payment Methods')

    # Display the plot
    plt.tight_layout()

    filename = 'graph22.png'

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