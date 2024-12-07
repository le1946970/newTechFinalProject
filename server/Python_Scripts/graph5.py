import matplotlib.pyplot as plt
import numpy as np
import pymongo
import pandas as pd
import sys
import os
from dotenv import load_dotenv

class BubbleChart:
    def __init__(self, area, bubble_spacing=0):
        area = np.asarray(area)
        r = np.sqrt(area / np.pi)
        self.bubble_spacing = bubble_spacing
        self.bubbles = np.ones((len(area), 4))
        self.bubbles[:, 2] = r
        self.bubbles[:, 3] = area
        self.maxstep = 2 * self.bubbles[:, 2].max() + self.bubble_spacing
        self.step_dist = self.maxstep / 2

        length = np.ceil(np.sqrt(len(self.bubbles)))
        grid = np.arange(length) * self.maxstep
        gx, gy = np.meshgrid(grid, grid)
        self.bubbles[:, 0] = gx.flatten()[:len(self.bubbles)]
        self.bubbles[:, 1] = gy.flatten()[:len(self.bubbles)]
        self.com = self.center_of_mass()

    def center_of_mass(self):
        return np.average(self.bubbles[:, :2], axis=0, weights=self.bubbles[:, 3])

    def center_distance(self, bubble, bubbles):
        return np.hypot(bubble[0] - bubbles[:, 0], bubble[1] - bubbles[:, 1])

    def outline_distance(self, bubble, bubbles):
        center_distance = self.center_distance(bubble, bubbles)
        return center_distance - bubble[2] - bubbles[:, 2] - self.bubble_spacing

    def check_collisions(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return len(distance[distance < 0])

    def collides_with(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return np.argmin(distance, keepdims=True)

    def collapse(self, n_iterations=50):
        for _i in range(n_iterations):
            moves = 0
            for i in range(len(self.bubbles)):
                rest_bub = np.delete(self.bubbles, i, 0)
                dir_vec = self.com - self.bubbles[i, :2]
                dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                new_point = self.bubbles[i, :2] + dir_vec * self.step_dist
                new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                if not self.check_collisions(new_bubble, rest_bub):
                    self.bubbles[i, :] = new_bubble
                    self.com = self.center_of_mass()
                    moves += 1
                else:
                    for colliding in self.collides_with(new_bubble, rest_bub):
                        dir_vec = rest_bub[colliding, :2] - self.bubbles[i, :2]
                        dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                        orth = np.array([dir_vec[1], -dir_vec[0]])
                        new_point1 = (self.bubbles[i, :2] + orth * self.step_dist)
                        new_point2 = (self.bubbles[i, :2] - orth * self.step_dist)
                        dist1 = self.center_distance(self.com, np.array([new_point1]))
                        dist2 = self.center_distance(self.com, np.array([new_point2]))
                        new_point = new_point1 if dist1 < dist2 else new_point2
                        new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                        if not self.check_collisions(new_bubble, rest_bub):
                            self.bubbles[i, :] = new_bubble
                            self.com = self.center_of_mass()

            if moves / len(self.bubbles) < 0.1:
                self.step_dist = self.step_dist / 2

    def plot(self, ax, labels, colors, percentages):
        for i in range(len(self.bubbles)):
            circ = plt.Circle(self.bubbles[i, :2], self.bubbles[i, 2], color=colors[i])
            ax.add_patch(circ)
            ax.text(*self.bubbles[i, :2], f"{percentages[i]:.1f}%", horizontalalignment='center', verticalalignment='center')

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
    
    if not reports_data:  # Check if there's no data
        print("no_data.png")
    else:
        # Convert the data to a pandas DataFrame
        reports_df = pd.DataFrame(reports_data)

        # Replace NaN or empty values in 'Payment Method' with 'Cash'
        reports_df['Payment Method'] = reports_df['Payment Method'].fillna('Cash')
        reports_df.loc[reports_df['Payment Method'] == '', 'Payment Method'] = 'Cash'

        # Modify the 'Payment Method' to handle commas
        def process_payment_method(payment_method):
            if ',' in payment_method:
                return 'Multiple payment methods'
            else:
                return payment_method.strip().title().replace('_', ' ')

        # Apply the process_payment_method function to each row in 'Payment Method'
        reports_df['Payment_Method'] = reports_df['Payment Method'].apply(process_payment_method)

        # Group by 'Payment_Method' and count occurrences
        payment_counts = reports_df['Payment_Method'].value_counts()

        # Check if there is data to plot
        if payment_counts.empty:
            print("No data available to display the plot.")
            return

        # Calculate the percentages for each payment method
        total = payment_counts.sum()
        percentages = (payment_counts.values / total) * 100

        # Define your new specific hex color codes
        color_hex_codes = [
            '#4156b4', '#7a44ad', '#a52395', '#c1006f', '#c90043', '#c60606'
        ]

        # Create a packed-bubble chart
        bubble_chart = BubbleChart(area=payment_counts.values, bubble_spacing=0.1)
        bubble_chart.collapse()

        # Create the figure with the desired size
        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(aspect="equal"))
        bubble_chart.plot(ax, payment_counts.index, color_hex_codes[:len(payment_counts)], percentages)
        ax.axis("off")
        ax.relim()
        ax.autoscale_view()
        ax.set_title('Most Popular Payment Methods')

        # Add legend
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) 
                for color in color_hex_codes[:len(payment_counts)]]
        ax.legend(handles, payment_counts.index, title="Payment Methods", loc="upper left", bbox_to_anchor=(1, 1))

        # Save the plot
        filename = 'packed_bubble_chart_with_legend.png'
        plt.savefig(filename, bbox_inches='tight')
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
