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


def createArchiProperties_csv_file(csv_fileFiltered, endpoint_name):
    combined_data = pd.DataFrame(columns=['ID', 'Key', 'Value'])

    # Iterate over rows in input CSV and append to combined_data
    for index, row in pd.read_csv(csv_fileFiltered).iterrows():
        instance_id = index + 1  # Starting ID from 1

        # Iterate over columns in the row
        for column in row.index:
            key = f'{column}'
            value = f'{row[column]}'
            combined_data = pd.concat([combined_data, pd.DataFrame({'ID': [f'{instance_id}'], 'Key': [key], 'Value': [value]})], ignore_index=True)

    # Read Anchor_NodeDescription_properties.csv'
    print(f"Reading file: Anchor_NodeDescription_properties.csv")
    Anchor_NodeDescription_properties = pd.read_csv('Anchor_NodeDescription_properties.csv')
    # Read csv_fileFiltered
    node_filtered = pd.read_csv(csv_fileFiltered)

    # Create a new DataFrame to store the combined data
    combined_data_properties = pd.DataFrame(columns=['ID', 'Key', 'Value'])

    # Iterate over rows in csv_fileFiltered and append to combined_data_node
    for index, row in node_filtered.iterrows():
        instance_id = index + 1  # Starting ID from 1

        # Iterate over columns in the row
        for column in node_filtered.columns:
            key = f'{column}'
            value = f'{row[column]}'
            combined_data_properties = pd.concat([combined_data_properties, pd.DataFrame({'ID': [f'{instance_id}'], 'Key': [key], 'Value': [value]})], ignore_index=True)

    # Append the combined_data to descriptionNodes_properties
    final_properties = pd.concat([ Anchor_NodeDescription_properties, combined_data_properties], ignore_index=True)

    # Save the updated dev_properties to a new CSV file
    final_properties.to_csv(f'{endpoint_name}_properties.csv', index=False)


#create updated element.csv
#number represents number of instances that will be listed in elements.csv
def CreateArchiElements_csv_file(csv_fileFiltered, endpoint_name, display):
    # Define the header and open the CSV file for writing
    header = ["ID", "Type", "Name", "Documentation", "Specialization"]

    # Create the output file name based on the input file name
    output_file = f'{endpoint_name}_elements.csv'

    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write the header
        writer.writerow(header)

        # Open the input CSV file to read 'Display' column
        with open(csv_fileFiltered, mode='r') as input_csv:
            reader = csv.DictReader(input_csv)

            # Generate rows with specified structure
            for i, row in enumerate(reader, start=1):
                # Use the value from the 'Display' column in the input CSV as the 'Name'
                node_name = row.get(display, '')  # the column 'display' has the names of the instances in Archi 

                # Create the row to be written in the output CSV
                output_row = [i, "Node", node_name, endpoint_name, ""]
                writer.writerow(output_row)

if __name__ == "__main__":

    # Get NetBox URL and API token interactively
    #netbox_url = input("Enter NetBox URL: ")
    #api_token = input("Enter API token: ")
    
    
    # Replace these values with your NetBox instance URL, API endpoint, and API token
    netbox_url = 'http://10.49.208.30:10150/api/'
    api_token = 'ae47c90213e877f716bc591a0ca65848ef7eb9fe'
   

  
   


    
    #devices CHECK
    desiredFields_devies = [ 'name', 'status.value', 'site.display', 'rack.display', 'device_type.display', 'position',
                       'device_role.display', 'device_type.manufacturer.display', 'serial', 'tenant.display'] 
    display_devies= 'name' 
    
   
    #Device Types CHECK
    desiredFields_deviceTypes = [ 'display', 'manufacturer.display', 'part_number', 'u_height', 'is_full_depth', 'device_count'] 
    display_deviceTypes = 'display'
     
    #Interfces 
   
    desiredFields_interfaces = [ 'display', 'device.display', 'label', 'enabled', 'type.label', 'description'] 
    display_interfaces = 'device.display'

    #racks
    desiredFields_racks = ['display', 'site.display', 'status.value', 'u_height', 'device_count', 'description']
    display_racks = 'display'

    #sites 
    desiredFields_sites = ['display', 'status.value', 'facility', 'region', 'group', 'tenant', 'description']
    display_sites = 'display'

    #tenats
    desiredFields_tenants = ['display',  'group',  'description']
    display_tenants = 'display'

    #cluster
    #desiredFields_clusters= []
    #display_clusters = ''

    #modules
    #VRF
    #VLAN
    #IP address 

    #Prefixes 
    desiredFields_prefixes = ['display',  'status.value', 'children', 'vrf', 'mark_utilized',  'tenant', 'site', 'vlan', 'role', 'description']
    display_prefixes  = 'display'







   
    # Specify the fields you want to include in the response

    # 1)under '/dcim' api endpoints:
    #  nodes devices : 'dcim/device/' 
    #  node device types : 'dcim/device-types/'
    #  node Interfaces : 'dcim/interfaces/'
    #  node racks
    #  node sites

    #2) under 'tenancy/tenants/':
    #    node tenants

    #3) under /api/virtualization/clusters/:
    #   node clusters

    #4) undr /api/ipam/prefixes/:
    # node prefixes 

 


    ###################
     # Define a list of API endpoints for the data you want to retrive from Netbox to loop over
    api_endpoints = [
        {'name': 'devices', 'endpoint': 'dcim/devices/', 'fields': desiredFields_devies, 'display': display_devies },
        {'name': 'device_types', 'endpoint': 'dcim/device-types/', 'fields': desiredFields_deviceTypes, 'display': display_deviceTypes},
        {'name': 'interfaces', 'endpoint': 'dcim/interfaces/', 'fields': desiredFields_interfaces, 'display': display_interfaces },
        {'name': 'racks', 'endpoint': 'dcim/racks/', 'fields': desiredFields_racks, 'display': display_racks },
        {'name': 'sites', 'endpoint': 'dcim/sites/', 'fields': desiredFields_racks, 'display': display_sites },
        {'name': 'tenants', 'endpoint': 'tenancy/tenants/', 'fields': desiredFields_tenants, 'display': display_tenants },
        # {'name': 'clusters', 'endpoint': 'virtualization/clusters/', 'fields': desiredFields_clusters, 'display': display_clusters  }
        {'name': 'prefixes', 'endpoint': 'ipam/prefixes/', 'fields': desiredFields_prefixes, 'display': display_prefixes }
    ]

    # Loop over API endpoints
    for endpoint in api_endpoints:
    # Specify the CSV file path -> Xfiltered.csv
    # this file contains all the filtered data of the Node we want to import into Archi 
    
        csv_fileFiltered = f'{endpoint["name"]}filtered.csv'

        # Fetch data from NetBox
        all_data = fetch_filtered_data(netbox_url, endpoint['endpoint'], api_token, endpoint['fields'])

        # Write data to a CSV file
        write_to_csv(all_data, csv_fileFiltered)

        # from Xfiltered.csv file  generate Xproperties.csv and Xelements.csv files, in respect to X. 
        createArchiProperties_csv_file( csv_fileFiltered, f'{endpoint["name"]}' )

   
        CreateArchiElements_csv_file( csv_fileFiltered, f'{endpoint["name"]}', f'{endpoint["display"]}')
