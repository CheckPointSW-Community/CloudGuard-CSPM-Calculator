# CloudGuard-CSPM-Calculator for Azure

## CloudGuard CSPM Calculator

This will help you calculate number of assets for CSPM and Log size for Threat Intelligence

## How to run the script

# Setup your account

- Paste the following into command prompt

    export AZURE_TENANT_ID="xxx"

    export AZURE_CLIENT_ID="xxx"

    export AZURE_CLIENT_SECRET="xxx"

    export SUBSCRIPTION_ID="xxx"

# Install requirements 

    pip3 install -r requirements.txt

# Run the script

    python3 d9-sizer.py

## Output


    ================================================================================================
    CloudGuard Azure Sizer - Report Summary
    ================================================================================================


    Total number of billable SQL Servers in Azure AD tenant xxx : 0
    Total number of billable virtual machines in Azure AD tenant xxx : 6
    Total number of billable functions in Azure AD tenant xxx : 3
    Total estimated flowlog storage used in Azure AD tenant xxx : 10394.97  MB


    Total number of CloudGuard billable assets licenses is : 6
