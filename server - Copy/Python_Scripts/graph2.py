import matplotlib.pyplot as plt
import pymongo
import pandas as pd
import numpy as np
import sys
import os
from dotenv import load_dotenv
from matplotlib.patches import ConnectionPatch

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

def plot_pie_chart_only(pie_ratios, pie_labels):
    """Plot only the pie chart with a larger circle."""
    fig, ax = plt.subplots(figsize=(10, 6))  # Standard figure size
    colors = ['#4156b4', '#863ea9', '#b50084', '#c8004f', '#c60606']  # Custom colors for pie chart
    ax.pie(
        pie_ratios, labels=pie_labels, autopct='%1.1f%%', pctdistance=0.85, labeldistance=1, wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'}, colors=colors
    )

    # Draw circle in the middle of the pie chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    
    # Add the circle on top of the pie chart
    fig.gca().add_artist(centre_circle)

    ax.set_title("Payment Methods")

    plt.tight_layout()

def plot_pie_and_bar_charts(pie_ratios, pie_labels, multiple_ratios, multiple_labels):
    """Plot both the pie chart and the bar chart."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
    fig.subplots_adjust(wspace=0)

    # Pie chart
    explode_label = 'Multiple payment methods'
    explode_index = pie_labels.index(explode_label) if explode_label in pie_labels else -1

    # Set initial values for 'explode'
    explode = [0.2 if i == explode_index else 0 for i in range(len(pie_ratios))]
    # Now, plot the pie chart
    angle = -180 * pie_ratios[explode_index] if explode_index >= 0 else 0

    colors = ['#4156b4', '#7a44ad', '#a52395', '#c1006f', '#c90043', '#c60606']  # Custom colors for pie chart
    wedges, *_ = ax1.pie(
        pie_ratios, labels=pie_labels, autopct='%1.1f%%', startangle=angle, explode=explode,
        pctdistance=0.75, labeldistance=1, wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'},
        colors=colors, radius=1.2
    )

    ax1.set_title("Payment Methods")

    # Draw circle in the middle of the pie chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white', zorder=10)
    ax1.add_artist(centre_circle)

    # Bar chart
    bottom = 1
    width = 0.2
    bar_colors = ['#4156b4', '#b50084', '#c60606']  # Custom colors for bar chart
    for j, (height, label) in enumerate(reversed(list(zip(multiple_ratios, multiple_labels)))): 
        bottom -= height
        bc = ax2.bar(0, height, width, bottom=bottom, color=bar_colors[j % len(bar_colors)], label=label)
        ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

    ax2.set_title("Multiple Payment Methods")
    ax2.legend()
    ax2.axis("off")
    ax2.set_xlim(-2.5 * width, 2.5 * width)

    # Connect the pie and bar charts
    theta1, theta2 = wedges[explode_index].theta1, wedges[explode_index].theta2
    center, r = wedges[explode_index].center, wedges[explode_index].r
    bar_height = sum(multiple_ratios)

    # Top connection line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(
        xyA=(-width / 2, bar_height), coordsA=ax2.transData, xyB=(x, y), coordsB=ax1.transData
    )
    con.set_color("black")
    con.set_linewidth(2)
    ax2.add_artist(con)

    # Bottom connection line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(
        xyA=(-width / 2, 0), coordsA=ax2.transData, xyB=(x, y), coordsB=ax1.transData
    )
    con.set_color("black")
    con.set_linewidth(2)
    ax2.add_artist(con)

    plt.tight_layout()

def plot_payment_methods(collectionReports):
    # Load data from MongoDB
    reports_data = list(collectionReports.find())
    reports_df = pd.DataFrame(reports_data)

    # Replace NaN or empty values in 'Payment Method' with 'Cash'
    reports_df['Payment Method'] = reports_df['Payment Method'].fillna('Cash')
    reports_df.loc[reports_df['Payment Method'] == '', 'Payment Method'] = 'Cash'

    # Process 'Payment Method' column
    def process_payment_method(payment_method):
        if ',' in payment_method:
            methods = [method.strip().title().replace('_', ' ') for method in payment_method.split(',')]
            methods.sort()
            reports_df.loc[reports_df['Payment Method'] == payment_method, 'Original_Payment_Methods'] = ' and '.join(methods)
            return 'Multiple payment methods'
        else:
            # Leave 'Original_Payment_Methods' empty for single payment methods
            reports_df.loc[reports_df['Payment Method'] == payment_method, 'Original_Payment_Methods'] = None
            return payment_method.strip().title().replace('_', ' ')

    reports_df['Payment_Method'] = reports_df['Payment Method'].apply(process_payment_method)

    # Filter for multiple payment methods
    multiple_payment_methods_df = reports_df[reports_df['Original_Payment_Methods'].notna()]

    # Pie chart data
    payment_counts = reports_df['Payment_Method'].value_counts()
    pie_ratios = payment_counts / payment_counts.sum()
    pie_labels = payment_counts.index.tolist()

    # Bar chart data (normalized ratios for multiple methods)
    multiple_ratios = multiple_payment_methods_df['Original_Payment_Methods'].value_counts()
    multiple_ratios = multiple_ratios / multiple_ratios.sum()
    multiple_labels = multiple_ratios.index.tolist()

    # Call appropriate function based on the presence of multiple payment methods
    if multiple_payment_methods_df.shape[0] > 0:
        plot_pie_and_bar_charts(pie_ratios, pie_labels, multiple_ratios, multiple_labels)
    else:
        plot_pie_chart_only(pie_ratios, pie_labels)

    filename = 'testt.png'
    plt.savefig(filename)
    print(filename)

def main():
    try:
        collectionReports = connect_mongodb()
        plot_payment_methods(collectionReports)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env
    main()
