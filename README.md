
![](images/logo.png)

# Table of content
* [ Introduction ](#introduction)  
* [ What is TheHive/Cortex ? ](#what-is-thehivecortex-)
* [ Use Cases ](#use-cases)
* [ Installation ](#installation)
	* [ Requirements ](#requirements)
	* [ Configuration ](#configuration)
		* [ Accounts ](#accounts)
		* [ TheHive/Cortex instances ](#thehivecortex-instances)
		* [ Logging ](#logging)
	* [ Refreshing the available analyzers ](#refreshing-the-available-analyzers)
* [ Usage ](#usage)
	* ["TheHive: Cases" dashboard](#thehive-cases-dashboard)
		* [ TheHive History ](#thehive-history)
		* [ Create a new case ](#create-a-new-case)
	* [ "Cortex: Jobs" dashboard ](#cortex-jobs-dashboard)
		* [ Cortex History ](#cortex-history)
		* [ Run new tasks ](#run-new-tasks)
	* [ Commands in searches ](#commands-in-searches)
* [ Support ](#support)
* [ Credits ](#credits)
* [ Licence ](#licence)

# Introduction
This TA allows to **add interaction features** between [TheHive or Cortex (TheHive project)](https://thehive-project.org/) and Splunk. It allows to retrieve all cases/jobs information from TheHive/Cortex and to perform actions on these instances using Splunk, from a search or from a predefined dashboard.
All data types work with the exception of "file" because Splunk does not allow to send a file easily.

This TA is supporting both versions of TheHive (3 and 4). It's also supporting the Cortex 3 version.

**Note**:
It's working using Python3 with the official thehive4py and cortex4api library included. Please note that few modifications were performed to avoid using the "magic" library which is difficult to add in this app.
**A support was added to use Python2**. This is not an official library, it's a syntactically-revised version.
This application is also available for Splunk version>7.x.

# What is TheHive/Cortex ?
If you need more information about TheHive/Cortex project, please [follow this link](https://thehive-project.org/).
You can find the related [TheHive Github here](https://github.com/TheHive-Project/TheHive) and [Cortex Github here](https://github.com/TheHive-Project/Cortex) .

# Use Cases
The objective is to interface a SIEM tool such as Splunk in order to be able to perform automated tasks on observables/IOCs.
This TA has been designed in such a way that :
* You can retrieve information from TheHive about the different cases that were created
* You can retrieve information from Cortex about the different jobs that are being performed on the scanners.
* You can create new case from Splunk in TheHive using the power of Splunk whether in a search or in a predefined dashboard.
* You can run new tasks from Splunk in Cortex using the power of Splunk whether in a search or a predefined dashboard.

# Installation
## Requirements
This application contains all the python libraries to work autonomously.

**However**, predefined dashboards of the application requires the installation of this application : [Status Indicator - Custom Visualization](https://splunkbase.splunk.com/app/3119/)

You should create a specific user and organization in your TheHive/Cortex instances to interact with Splunk.

## Configuration
Before using the application, you need to set up your environment settings. Please note that this application is using a list of accounts and instances, meaning you can configure several instances of TheHive/Cortex in the same app and with different accounts.

### Accounts

You have to set up your accounts/instances configuration.
An account is used to authenticate to one instance. You have to add every account you need to use and store the API Key as the password (**username/password authentication is only supported for TheHive, not Cortex, we recommand you to use an API key**)
1. Go to the **TheHive/Cortex application > Settings > Configuration** (in the navigation bar)
2. Under **Accounts**, you need to add any account you want to use with TheHive/Cortex
* **Account name**: The name of the account, it will be reused to link an account to an instance.  
* **Username**: The username of this account. For now, it's not used but we recommand you to keep the same name as you have on your instance (TheHive or Cortex)
* **Password**: The password field must be filled with **a valid API key** to use for authentification

![](images/accounts.png)
*This image is an example of one registered account named "Splunk_TheHive3"*

### TheHive/Cortex instances

Once you've done that, you can configure all your instances. An instance is an endpoint representing a TheHive or Cortex instance.
1. Go to the **TheHive/Cortex application > Settings > Instances** (in the navigation bar)
2. On this dashboard, you need to add every instance you want to use. To do so, select the "**Add a new instance**" as action and fill these fields:
- **Account name (Global accounts)**: This is the name of the account to use that you added under "Accounts". You can automatically fill this field by clicking on one row of the first search named "Global accounts detected" that list you all available accounts.
- **Authentication type**: Authentication type for your instance. Password is working only with TheHive but we recommand you to use an API key everytime
- **Type**: Type of your instance (TheHive (v3 or v4) or Cortex (v3))
- **Organisation**: The name of the organisation against which api calls will be run. Defaults to "-" meaning None
- **Protocol**: Protocol to use (HTTP or HTTPS). Default to HTTP.
- **Certificate Verification**: Indicate if the certificate verification is required. If you use an HTTPS connection with a self-signed certificate of a custom certificate authority, you must add your trusted certificate to the "certifi" library. To do so, append your certificate under "\$APP_FOLDER\$/bin/ta_thehive_cortex/aob_py3/certifi/cacert.pem" (or aob_py2 if you use Python 2.7). Default to True
- **Proxies**: A dictionary of proxies if needed. If you don't use any proxy, set this input as default ({}). If you use a proxy, it's expecting a dictionary of two keys ("http" and "https") with the proxy value as dictionary value. **Example**: {"http": "http://my_proxy:8080", "https": "http://my_proxy:8080"}
- **Host**: Host of your instance (hostname or IP)
- **Port**: Port used by your instance (Default:9000 for TheHive, 9001 for Cortex)


![](images/instances_add.png)
*This image shows the addition of a new instance (partially filled fields) by specifying an account name defined beforehand.*

On the above example, you can see a list of defined instances.

### Logging

You can enable a "debug" logging mode (under **Configuration**) to have more information in searches/logs.
By default, a logging file is created under `$SPLUNK_HOME/var/log/splunk/` with the file name starting with "command_"

You will be able to have these logs in your search.log.

## Refreshing the available analyzers
Once you've configured your Cortex input, the list of analyzers will be loaded in Splunk.
Each time the supervisor script is checking the connection, it will recover the list of analyzers to keep it up to date.

![](images/analyzers.png)

**Note**: Only enabled analyzers will be loaded

These information are stored in Splunk in order to have a mapping between available analyzers and data types.


# Usage
Once the application is configured and the analyzers are loaded, you have several options for interfacing with TheHive/Cortex.
## "TheHive: Cases" dashboard
The application integrates a preconfigured dashboard with searches allowing you to easily interface with TheHive.

![](images/cases_list.png)

### TheHive History
You can retrieve the history of cases in TheHive using the action "LIST".
For each job, you can see :
* **TLP**: TLP of the case
* **Title**: Title of the case
* **Tags**: Tags of the case
* **Severity**: Severity of the case
* **Tasks**: Tasks of the case by status
* **Observables**: Number of observables for the case
* **Assignee**: Current assignee for the case
* **Start Date**: Date and time for the start of the case
* **Metrics**: Current metrics for the case
* **Custom Fields**: Current custom fields for the case
* **Status**: Current status for the case with detailed resolution
* **ID**: ID of the job

**Note: You can click on the ID to view the result of the job directly on TheHive** (you should be authenticated to TheHive)

You can set filters for the history:
* **Keyword**: A keyword to search on
* **Status**: Status of the case
* **Severity**: Severity of the case
* **Tags**: Tags of the case
* **Title**: Title of the case
* **Assignee**: Assignee of the case
* **Date**: Creation date of the case

### Create a new case
You can create a new case from Splunk using the "CREATE" action.

![](images/cases_create.png)

You have to specify some inputs:
* **Title**: Title for this new case
* **Severity**: Severity for this new case
* **Tags**: Tags for this new case (they are added by specifiying values in the "Enter a new tag" input)
* **Tasks**  Tasks for this new case (they are added by specifying values in the "Enter a new task" input)
* **TLP**: TLP for this new case
* **PAP**: PAP for this new case
* **Description**: Description for this new case

The search will create the new case and return information such as the job ID.

## "Cortex: Jobs" dashboard
The application integrates a preconfigured dashboard with searches allowing you to easily interface with Cortex.

![](images/jobs_list.png)

### Cortex History
You can retrieve the history of jobs in Cortex using the action "LIST".
For each job, you can see :
* **Status**: Current status for the job
* **Data**: Data and datatype for the job
* **Analyzer**: Analyzer used for the job
* **Created At**: Date and time for the creation of the job
* **Start Date**: Date and time for the start of the job (a created job could not be executed immediately)
* **Created by**: User/Organization used to created the job
* **TLP**: TLP specified for the job
* **ID**: ID of the job

**Note: You can click on the ID to view the result of the job directly on Cortex** (you should be authenticated to Cortex)

You can set filters for the history:
* **Data**: filtering the "data" field, regular expressions are not working, it must be the exact match string
* **Data Types**: filtering on the "data types", several values can be specified
* **Analyzers**: filtering on the "analyzers", several values can be specified

### Run new tasks
You can start new analyses from Splunk using the "RUN" action.

![](images/jobs_run.png)

You have to specify some inputs:
* **Data**: data you want to analyze separated by a semicolon, they must be of the same data type
* **Data type**: corresponding to the data type of data
* **TLP**: TLP level to use for this analysis
* **PAP**  PAP level to use for this analysis
* **Analyzers**: analyzers to use, if "any" is set, it will use any enabled analyzers for the given data type

The search will execute all jobs (one data with one analyzer) and return information such as the job ID.

## Commands in searches
You can use new commands within your searches. For more information, please [read the associated documentation](https://github.com/LetMeR00t/TA-cortex/tree/master/docs/commands.md).
# Support
Please [open an issue on GitHub](https://github.com/LetMeR00t/TA-cortex/issues) if you'd like to report a bug or request a feature.

# Credits
This app was inspired by [this Splunk app](https://splunkbase.splunk.com/app/4380/)

# Licence
This app TA_cortex is licensed under the GNU Lesser General Public License v3.0.

