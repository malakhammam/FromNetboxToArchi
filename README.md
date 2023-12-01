# FromNetboxToArchi
Scripts automates data transfer from Netbox to Archi.

The following steps are repeated for every field in netbox that we want to store instances from in Archi:

1) The filtered data from Netbox is fetched and stored in Nodefiltered.csv
2) Node_properties.csv is created by copying the content of Nodefiltered.csv and giving it the following structure:
   Every Node_properties.csv file's header consists of  "ID","Type","Name".
   This structure allows for the file to be imported in Archi.
3) Node_elements.csv is created.
   Every Node_elements.csv file's header consists of "ID","Type","Name","Documentation","Specialization".
   'Type' is set to Node.
   For 'Name' the name of the instances gets copied from Nodefiltered.csv.
