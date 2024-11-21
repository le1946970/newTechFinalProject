# imports
import pandas as pd
import sys
from pymongo import MongoClient

# mongodb connection setup
cluster_uri = "mongodb+srv://newTechPi:ggE84XiHnMBjXr7@clusternewtech.h05cs.mongodb.net/?retryWrites=true&w=majority&appName=clusterNewTech"

client = MongoClient(cluster_uri)
db = client['newTech']
collection = db['reports']

def import_data(report_filename):
    # reading report.csv
    report_df = pd.read_csv(report_filename)
    
    # filtering the data to include records where "POS Location Name" is "215 Rue Queen" or "Mackey - 215 Rue Queen"
    valid_locations = ["215 Rue Queen", "Mackey - 215 Rue Queen"]
    filtered_data = report_df[report_df['POS Location Name'].isin(valid_locations)]
    
    # converting filtered data to dict
    data_dict = filtered_data.to_dict(orient='records')

    # inserting into mongodb
    collection.insert_many(data_dict)
    print("Data imported successfully")

# checking for error
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage is : python file_name.py <report_filename>")
        sys.exit(1)

    # arguments
    report_filename_arg = sys.argv[1]
    
    # calling function using arguments
    import_data(report_filename_arg)
