# FromNetboxToArchi 

This Python script interacts with the NetBox API to fetch data of various specified Network elements. It then processes the retrieved data and creates CSV files suitable for import into the modeling tool Archi. Let's break down the script step by step:

1. **Function: fetch_filtered_data**
   - Takes parameters for the NetBox API URL, initial API endpoint, API token, and fields to retrieve.
   - Sends HTTP GET requests to the NetBox API using the `requests` library.
   - Handles pagination, combining results from multiple pages.
   - Filters and extracts specified fields from the JSON response.
   - Returns a list of dictionaries containing filtered data.

2. **Function: nested_field**
   - A utility function that helps access nested fields within a dictionary.

3. **Function: write_to_csv**
   - Writes the filtered data to a CSV file using the `csv` module.
   - The CSV file path and data are provided as parameters.

4. **Function: createArchiProperties_csv_file**
   - Combines data from the filtered CSV file with an existing properties CSV file related to NodeDescription.
   - Concatenates and saves the result to a new CSV file, updating properties for Archi.

5. **Function: CreateArchiElements_csv_file**
   - Creates a new elements CSV file based on the filtered CSV data.
   - Generates a row for each instance.
   - The headers consist of "ID","Type","Name","Documentation","Specialization".
   - Uses the 'Display' column from the filtered CSV as the 'Name' in the elements.CSV being created for Archi.

6. **Main Block:**
   - Collects NetBox URL and API token interactively from the user.
   - Defines API endpoints for various elements in Netbox, each with specified fields and a display column.
   - Iterates over the defined endpoints and performs the following for each:
     - Fetches filtered data from NetBox using `fetch_filtered_data`.
     - Writes the filtered data to a CSV file using `write_to_csv`.
     - Creates for Archi properties.CSV using `createArchiProperties_csv_file`.
     - Creates for Archi elements.CSV using `CreateArchiElements_csv_file`.

7. **Notes:**
   - It interacts with the NetBox API, so you need to replace the user input section with the actual NetBox URL and API token.
   - The CSV file paths, desired fields, and display columns for each endpoint are configurable.
