import requests
import csv
import pandas as pd

def fetch_filtered_data(api_url, initial_api_endpoint, api_token, fields):
    # Set up the headers with the API token
    headers = {
        'Authorization': f'Token {api_token}',
        'Content-Type': 'application/json',
    }

    # Initialize an empty list to store all data
    all_data = []

    # Initial page URL
    page_url = f'{api_url}{initial_api_endpoint}'

    # Pagination loop
    while page_url:
        # Make the API request
        response = requests.get(page_url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract only the desired fields from each item in the list
            filtered_data = [{field: item.get(field) if '.' not in field else nested_field(item, field.split('.')) for field in fields} for item in data['results']]

            # Extend the list with filtered data from the current page
            all_data.extend(filtered_data)

            # Update the API endpoint for the next page
            page_url = data['next']
        else:
            # Print an error message and break the loop if the request fails
            print(f'Error: Unable to fetch data. Status code: {response.status_code}')
            print(response.text)
            break

    return all_data

def nested_field(item, field_list):
    """
    Access nested fields in the item dictionary.
    """
    current_level = item
    for field in field_list:
        current_level = current_level.get(field, {})
         
        if current_level is None:
            return None
    return current_level

def write_to_csv(data, csv_file_path):
    # Specify the CSV file path
    with open(csv_file_path, 'w', newline='') as csvfile:


     

        
        # Extract fieldnames from the first record in the data (assuming there is data)
        fieldnames = list(data[0].keys()) if data else []

        # Create a CSV DictWriter
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write CSV header
        writer.writeheader()

        # Write data rows
        writer.writerows(data)


#create updated element.csv
#create updated element.csv
#number represents number of instances that will be listed in elements.csv
def generate_csv_file(input_csv_file, output_file):
    # Define the header and open the CSV file for writing
    header = ["ID", "Type", "Name", "Documentation", "Specialization"]

    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write the header
        writer.writerow(header)

        # Open the input CSV file to read 'Display' column
        with open(input_csv_file, mode='r') as input_csv:
            reader = csv.DictReader(input_csv)

            # Generate rows with specified structure
            for i, row in enumerate(reader, start=1):
                # Use the value from the 'Display' column in the input CSV as the 'Name'
                node_name = row.get('device.display', '')  # Get the value with a fallback to an empty string

                # Create the row to be written in the output CSV
                output_row = [i, "Node", node_name, "", ""]
                writer.writerow(output_row)

                # Print information for debugging
                #print(f"Processed row {i}: Name = {node_name}")

    print(f'Data successfully exported to {output_file}')


if __name__ == "__main__":
    # Replace these values with your NetBox instance URL, API endpoint, and API token
    netbox_url = 'http://10.49.208.30:10150/api/'
    #1)
    # under '/dcim' api endpoints:
    #  nodes devices : 'dcim/device/' 
    #  node device types : 'dcim/device-types/'
    # node Interfaces : 'dcim/interfaces/'
     # Specify the API endpoint for the data you want to retrieve
    initial_api_endpoint = 'dcim/interfaces/'
    ###api_endpoint = 'dcim/interfaces/'  # Specify the API endpoint for the data you want to retrieve

    api_token = 'ae47c90213e877f716bc591a0ca65848ef7eb9fe'
    # Specify the fields you want to include in the response

    #dcim endpoints
    '''  
    #devices CHECK
    desired_fields = [ 'name', 'status.value', 'site.display', 'rack.display', 'device_type.display', 'position',
                       'device_role.display', 'device_type.manufacturer.display', 'serial', 'tenant.display']  '''
    #device_roles ,didnt model in archi so far
    ''' desired_fields = [ 'name', 'device_count', 'virtualmachine_count', 'color', 'vm_role', 'description'] '''
   
    #Device Types CHECK
    '''desired_fields = [ 'display', 'manufacturer.display', 'part_number', 'u_height', 'is_full_depth', 'device_count'] '''
     
    #Interfces 
    desired_fields = [ 'display', 'device.display', 'label', 'enabled', 'type.label', 'description'] 
    
    #cables
    ''' desired_fields = [ 'a_terminations.device.display', 'b_terminations.device.display', 'a_terminations.display', 'b_terminations.display', 'status.value',
      'type', 'description', 'length', 'RACKA', 'RACKB'] '''
    
    #
    #
    #
    #
    #
    #

    

    # Specify the CSV file path 
    # This File will include all the properties that want to be transferred to archimate 
    ##############ADAPT the name for nodefiltered_properties.csv
    csv_file_path = 'interfacesfiltered.csv'
    

    # Fetch all data from NetBox
    all_data = fetch_filtered_data(netbox_url,  initial_api_endpoint, api_token, desired_fields)

    # Write the data to a CSV file
    write_to_csv(all_data, csv_file_path)
    
    print(f'Data successfully exported to {csv_file_path}')




    # Read 'dev_properties.csv'
    descriptionNodes_properties = pd.read_csv('interfaces_NodeDescription_properties.csv')
    #Read 'node_filtered_properties.csv'
    ##############ADAPT the name for nodefiltered_properties.csv
    node_filtered = pd.read_csv('interfacesfiltered.csv')
    # Create a new DataFrame to store the combined data
    combined_data = pd.DataFrame(columns=['ID', 'Key', 'Value'])
    
    # Iterate over rows in 'devfiltered2.csv' and append to 'combined_data'
    for index, row in node_filtered.iterrows():
        instance_id = index + 1  # Starting ID from 1
        #The inner loop iterates over each column in the node_filtered DataFrame.
        for column in node_filtered.columns:
            key = f'{column}' # Sets the 'Key' column in the new DataFrame to the name of the current column.
            value = f'{row[column]}' #  Sets the 'Value' column to the value in the current row and column of node_filtered.
            combined_data = pd.concat([combined_data, pd.DataFrame({'ID': [f'{instance_id}'], 'Key': [key], 'Value': [value]})], ignore_index=True)
    
    
    # Append the combined_data to dev_properties
    dev_properties = pd.concat([descriptionNodes_properties, combined_data], ignore_index=True)

    # Save the updated dev_properties to a new CSV file
    dev_properties.to_csv('interfaces_properties.csv', index=False)

    # Example usage:
    generate_csv_file( "interfacesfiltered.csv", "interfaces_elements.csv")



    





    


    ##########

  