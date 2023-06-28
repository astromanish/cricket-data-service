#### Cricket Data Service

### Overview
The Cricket Data Service is a comprehensive and professional system designed to collect, process, store, and provide services over cricket-related data. It follows a streamlined data flow process that involves the following categories of steps:

## Data Collection and Storage:
- Fetched from APIs: The system retrieves cricket data from the reliable Sport related APIs.
- Stored into Proper Folder Structure: The fetched data is organized and stored in a well-structured folder hierarchy for efficient data management.
## Data Processing and Transformation:
- Loaded into pandas Dataframe: The data is loaded into a pandas Dataframe, enabling powerful data manipulation and analysis capabilities.
- Data Cleaning: Data cleaning operations are performed to ensure data accuracy and consistency.
## Data Enrichment and Consolidation:
- Additional Column Addition and Dataframe Merging: Relevant additional columns are added to enrich the dataset, and the data is merged into a temporary Dataframe.
- Final Dataframe Creation: From the temporary Dataframe, the final Dataframe for each item mentioned in the schema file is derived.
## Data Storage and Services:
- Writing to Delta Lake: The final Dataframe, containing processed and refined cricket data, is securely written to Delta Lake, ensuring efficient storage and retrieval.
- Providing various cricket-related APIs over the stored data: The Cricket Data Service offers a range of APIs that enable users to access and utilize the cricket data for analysis, research, and decision-making purposes.

For detailed instructions on setting up and utilizing the Cricket Data Service, please refer to the comprehensive technical documentation. It provides step-by-step guidance and additional information to help you make the most of the service.