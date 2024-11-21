import matplotlib.pyplot as plt
import pymongo
import pandas as pd
import sys
import os
import numpy as np
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

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
    fig.subplots_adjust(wspace=0)

    labels=payment_counts.index
    label_to_explode = 'Multiple payment methods'

    # Find the index of the label to explode
    explode = [0] * len(labels)  # Start with no explode
    if label_to_explode in labels:
        explode[labels.index(label_to_explode)] = 0.1  # Explode the specific label
    # Find the index of the label to align to the right

    label_index = labels.index(label_to_explode)

    # Calculate the cumulative proportion of the slices before the target label
    cumulative_sum = sum(payment_counts[:label_index])

    # Calculate the angle to align the target label to the right
    # Since the sum equals 1, we can directly calculate the angle from the cumulative sum
    angle = -180 * (cumulative_sum)  # Negative for counterclockwise rotation
    wedges, *_ = ax1.pie(payment_counts, autopct='%1.1f%%', startangle=angle,
                        labels=labels, explode=explode)
    
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

'''
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import ConnectionPatch

# make figure and assign axis objects
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
fig.subplots_adjust(wspace=0)

# pie chart parameters
overall_ratios = [.27, .56, .17]
labels = ['Approve', 'Disapprove', 'Undecided']
explode = [0.1, 0, 0]
# rotate so that first wedge is split by the x-axis
angle = -180 * overall_ratios[0]
wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                     labels=labels, explode=explode)

# bar chart parameters
age_ratios = [.33, .54, .07, .06]
age_labels = ['Under 35', '35-49', '50-65', 'Over 65']
bottom = 1
width = .2

# Adding from the top matches the legend.
for j, (height, label) in enumerate(reversed([*zip(age_ratios, age_labels)])):
    bottom -= height
    bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                 alpha=0.1 + 0.25 * j)
    ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

ax2.set_title('Age of approvers')
ax2.legend()
ax2.axis('off')
ax2.set_xlim(- 2.5 * width, 2.5 * width)

# use ConnectionPatch to draw lines between the two plots
theta1, theta2 = wedges[0].theta1, wedges[0].theta2
center, r = wedges[0].center, wedges[0].r
bar_height = sum(age_ratios)

# draw top connecting line
x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = r * np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
con.set_linewidth(4)
ax2.add_artist(con)

# draw bottom connecting line
x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = r * np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(4)

plt.show()
'''