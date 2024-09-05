# Function to merge JSON files

    # Format of the JSON data:
    # 
    #  { 
    #   "employee_id": "EMP001",
    #    "week_start": "2024-08-25", 
    #    "availability": [
    #      {
    #        "day": "Monday",
    #        "available_from": "10:00:00", 
    #        "available_to": "12:00:00"
    #      },
    #      {
    #        "day": "Monday",
    #        "available_from": "18:00:00", 
    #        "available_to": "20:00:00"
    #      },
    #      {
    #        "day": "Monday",
    #        "available_from": "23:00:00", 
    #        "available_to": "00:00:00"
    #      },
    #      {
    #        "day": "Tuesday",
    #        "available_from": "00:00:00",
    #        "available_to": "01:30:00"
    #      },
    #      {
    #        "day": "Saturday",
    #        "available_from": "08:30:00",
    #        "available_to": "16:30:00"
    #      }
    #    ]
    #  }
    #
    # The JSON files are stored in the /downloads directory

import os
import json
from datetime import datetime

# Variables storing the accepted employee IDs
accepted_employee_ids = ['EMP001', 'EMP002', 'EMP003', 'EMP004', 'EMP005']

def merge_files():
    # Directory containing the JSON files
    downloads_dir = 'downloads'
    combined_dir  = 'downloads\combined'
    
    # List to hold the combined data
    combined_data = []
    users_in_this_list = [] 
     
    # Scan the /downloads directory for JSON files and read the data inside each file
    for file in os.listdir(downloads_dir):
        if file.endswith('.json'):
            with open(os.path.join(downloads_dir, file), 'r') as f:
                data = json.load(f)
                # At this point we need to check if the data contains the right data
                if not isinstance(data, dict):
                    print(f"Data in {file} is not in the correct format. FORMAT ERROR!!!")
                    #save the employee_id in a variable like for a list
                    #Extra warning for the user
                    print("THIS FILE WILL BE IGNORED!!!")
                    continue 
                else:
                    #print(f"Data in {file} is in the correct format.It is a dictionary.")
                    #save the employee_id and week_start in a variable
                    this_employee_id = data["employee_id"]
                    this_week_start = data["week_start"]

                    # 1. Check if the employee_id is one of the accepted employee IDs
                    if this_employee_id in accepted_employee_ids:
                        #print(f"Employee ID {this_employee_id} is accepted.")
                        # 2. Check if the employee_id is already in the list
                        if this_employee_id in users_in_this_list:
                            print(f"Employee is already in the list. OVERLAP DETECTED!")
                            continue
                        else:
                            #print(f"Employee is not in the list.")
                            # Check if the week_start is acceptable
                            week_start_date = datetime.strptime(this_week_start, '%Y-%m-%d')
                            # Check if the week_start_date is in the future
                            if week_start_date < datetime.now():
                                print(f"week_start_date {week_start_date} is in the past. OLD FILES!")
                                continue
                            else:
                                print(f"week_start_date {week_start_date} is in the future. This file will be accepted and included in the final file.")
                                # Add the data to the combined data list
                                combined_data.append(data)
                                # Add the employee_id to the list of users
                                users_in_this_list.append(this_employee_id)

                    else:
                        print(f"Employee ID {this_employee_id} is not accepted. NOT A MEMBER!")
                        continue
                    

    # Create a new JSON file with the combined data and save it in the /combined directory

    combined_file_path = os.path.join(combined_dir, f'combined_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json')

    with open(combined_file_path, 'w') as f:
        json.dump(combined_data, f, indent=4)
    # End of function messages
    print(f'Combined JSON file created at {combined_file_path}')
    print("All JSON files have been merged.")
