# CloudGuard-CSPM-Calculator for Azure

## CloudGuard CSPM Calculator

This will help you calculate number of assets for CSPM and Log size for Threat Intelligence

## How to run the script

This script can be run with your environmental variables set to point to your Azure Cloud Account (or service principle) or by logging into the Azure Cli with "az login".

Using environmental variables with a service principle account that has access to all subscriptions in this tenant is recommended.  If you use your "az login", the account must have permissions to all subscriptions or the calculations will be off.
 
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
    
 ### This project originated by the github user chrisbeckett
