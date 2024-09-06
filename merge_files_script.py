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
from datetime import datetime, timedelta

# Variables storing the accepted employee IDs
accepted_employee_ids = ['EMP001', 'EMP002', 'EMP003', 'EMP004', 'EMP005']
# Function to get the week number from a date
def week_number(date):
    return date.isocalendar()[1]

def merge_files():
    # Directory containing the JSON files
    downloads_dir = 'downloads'
    combined_dir  = 'downloads\combined'
    
    # List to hold the combined data
    combined_data_this_week = []
    combined_data_next_week = []
    combined_data_nnext_week = []
    user_list_this_w = []
    user_list_next_w = []
    user_list_nnext_w = []
    #week_no = week_number(datetime.now())
     
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
                    #save the employee_id in a variable
                    this_employee_id = data["employee_id"]

                    # 1. Check if the employee_id is one of the accepted employee IDs
                    if this_employee_id in accepted_employee_ids:
                        #print(f"Employee ID {this_employee_id} is accepted.")
                        
                        # Check if the week_start is acceptable
                        date_in_this_json = datetime.strptime(data["week_start"], '%Y-%m-%d')
                        week_no_in_this_json = week_number(date_in_this_json)
                        week_no_now = week_number(datetime.now())
                        week_no_next = week_no_now + 1
                        week_no_next_n = week_no_now + 2
                        next_monday = datetime.now() + timedelta(days=-datetime.now().weekday(), weeks=1)
                        nnext_monday = datetime.now() + timedelta(days=-datetime.now().weekday(), weeks=2)
                        last_monday = datetime.now() + timedelta(days=-datetime.now().weekday())

                        # Check if the date_in_this_json is too old (7 days in the past)
                        if date_in_this_json < datetime.now() - timedelta(days=7):
                            print(f"date_in_this_json {date_in_this_json} is in the past. OLD FILES!")
                            continue
                        else:
                            #print(f"date_in_this_json {date_in_this_json} is in the future. This file will be accepted and included in the final file.")
                            # Check for which week is this set of data (it can be the first coming week, the second coming week, etc.)
                            
                            # 1. coming week - normal scenario
                            if week_no_in_this_json == week_no_next:
                                print(f"This data is for the coming week: {week_no_next}")
                                # check the monday
                                date_in_this_json = date_in_this_json.date()
                                next_monday = next_monday.date()
                                if date_in_this_json == next_monday:
                                    print(f"This data is for next monday: {next_monday}")
                                    combined_data_next_week.append(data)
                                    # Add the employee_id to the list of users
                                    user_list_next_w.append(this_employee_id)
                                else:
                                    print(f"This data is not for A monday.")
                                    continue
                            
                            # 2. next coming week - special scenario
                            elif week_no_in_this_json == week_no_next_n:
                                print(f"This data is for the next coming week: {week_no_next_n}")
                                # check the monday
                                date_in_this_json = date_in_this_json.date()
                                nnext_monday = nnext_monday.date()
                                if date_in_this_json == nnext_monday:
                                    print(f"This data is for next monday: {nnext_monday}")
                                    combined_data_nnext_week.append(data)
                                    # Add the employee_id to the list of users
                                    user_list_nnext_w.append(this_employee_id)
                                else:
                                    print(f"This data is not for A monday.")
                                    continue

                            # 3. this week - late scenario
                            elif week_no_in_this_json == week_no_now:
                                print(f"This data is for this week: {week_no_now}")
                                # check the monday
                                date_in_this_json = date_in_this_json.date()
                                last_monday = last_monday.date()
                                if date_in_this_json == last_monday:
                                    print(f"This data is for last monday: {last_monday}")
                                    combined_data_this_week.append(data)
                                    # Add the employee_id to the list of users
                                    user_list_this_w.append(this_employee_id)
                                else:
                                    print(f"This data is not for A monday.")
                                    continue
                            else:
                                print(f"This data is too far in the future. NOT ACCEPTED!")
                                continue
                    
                    else:
                        print(f"Employee ID {this_employee_id} is not accepted. NOT A MEMBER!")
                        continue
                    

    # Create a new JSON file with the combined data and save it in the /combined directory
    # Create three files for the three different weeks
    # Week - Normal scenario  
    # if data is for next week, store it in a file with the name komb_<week_no_next_n>_next_<date+time(no seconds).json>
    combined_file_path_one = os.path.join(combined_dir, f'komb_{week_no_next}_next_{datetime.now().strftime("%Y-%m-%d_%H-%M")}.json')
    with open(combined_file_path_one, 'w') as f:
        json.dump(combined_data_next_week, f, indent=4)
    
    # Week - Late scenario
    combined_file_path_two = os.path.join(combined_dir, f'komb_{week_no_now}_last_{datetime.now().strftime("%Y-%m-%d_%H-%M")}.json')
    with open(combined_file_path_two, 'w') as f:
        json.dump(combined_data_this_week, f, indent=4)

    # Week - Special scenario
    combined_file_path_three = os.path.join(combined_dir, f'komb_{week_no_next_n}_next_{datetime.now().strftime("%Y-%m-%d_%H-%M")}.json')
    with open(combined_file_path_three, 'w') as f:
        json.dump(combined_data_nnext_week, f, indent=4)


    # End of function messages
    print(f'Combined JSON file created at {combined_file_path_one}')
    print(f'Combined JSON file created at {combined_file_path_two}')
    print(f'Combined JSON file created at {combined_file_path_three}')

    print("All JSON files have been merged.")





# Call the function to merge the JSON files
merge_files()