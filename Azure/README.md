# CloudGuard-CSPM-Calculator for Azure

## CloudGuard CSPM Calculator

This will help you calculate number of assets for CSPM and Log size for Threat Intelligence

## How to run the script

This script can be run with your environmental variables set to point to your Azure Cloud Account (or service principle) or by logging into the Azure Cli with "az login".

Using environmental variables with a service principle account that has access to all subscriptions in this tenant is recommended.  If you use your "az login", the account must have permissions to all subscriptions or the calculations will be off.

*You can also choose to run the script with a known access token. You can get an access token by opening up the azure CLI and running the command "az account get-access-token".
If you want a specific subscription access token you can run the same command with "--subscription subscriptionID", where the subscription id is the id of the specific subscription that you want to get the access token for. 
The whole command should look like this if you were using a subscription ID:

az account get-access-token --subscription 0000000-0000-0000-0000-000000000000

Then copy what azure returns which should start and end with "{" and "}" and run it with the following command (the single quotes are required):

TODO //Add Example of how to run

python sizer-with-input-token.py 'accessToken'

Where the accessToken is what you copied and from the azure CLI.

# Setup your account

    export AZURE_TENANT_ID="xxx"
    export AZURE_CLIENT_ID="xxx"
    export AZURE_CLIENT_SECRET="xxx"
    export SUBSCRIPTION_ID="xxx"
OR
    az login 
      (opens a browser for authentication)
OR
    az login --use-device-code

# Install requirements 

    pip3 install -r requirements.txt

# Run the script

    python3 d9-sizer.py

## Output


    ================================================================================================
    CloudGuard Azure Sizer - Report Summary
    ================================================================================================


    Total number of billable SQL Servers in Azure AD tenant : 0
    Total number of billable virtual machines in Azure AD tenant : 6
    Total number of billable functions in Azure AD tenant : 3
    Total estimated flowlog storage used in Azure AD tenant : 10394.97  MB


    Total number of CloudGuard billable assets licenses is : 6
    
 ### Credit
 This project originated by the github user chrisbeckett
