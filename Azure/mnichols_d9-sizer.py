# This script logs into Azure AD and iterates through subscriptions to onboard them into CloudGuard
# Feedback to chrisbe@checkpoint.com or open an issue on https://github.com/chrisbeckett/d9-azure-sizer/issues

# To run the script, you will need to set environment variables for AZURE_CLIENT_ID, AZURE_CLIENT_SECRET and AZURE_TENANT_ID

# Import required libraries
import os
import sys
import logging
import datetime
import json
from azure.identity import ClientSecretCredential
#from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.subscription.operations import SubscriptionsOperations
from msrestazure.azure_exceptions import CloudError
from azure.mgmt.compute import ComputeManagementClient
from colorama import Fore,init
from azure.mgmt.web import WebSiteManagementClient
from azure.core.exceptions import HttpResponseError

from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.monitor import MonitorManagementClient

init()

# Verify the environment variables have been set

def verify_env_variables():
    try:
        if 'AZURE_TENANT_ID' in os.environ:
            pass
        else:
            print("ERROR : The Azure AD tenant ID has not been defined in environment variables")
            sys.exit(0)
        if 'AZURE_CLIENT_ID' in os.environ:
            pass
        else:
            print("ERROR : The Azure AD application ID has not been defined in environment variables")
            sys.exit(0)
        if 'AZURE_CLIENT_SECRET' in os.environ:
            pass
        else:
            print("ERROR : The Azure AD application secret key has not been defined in environment variables")
            sys.exit(0)
    except:
        sys.exit(0)

verify_env_variables()

# Set Azure AD credentials from the environment variables

credentials = ClientSecretCredential(
    client_id=os.environ['AZURE_CLIENT_ID'],
    client_secret=os.environ['AZURE_CLIENT_SECRET'],
    tenant_id=os.environ['AZURE_TENANT_ID']
 )

# Read in required environment variables
az_tenant=os.environ['AZURE_TENANT_ID']
az_appid=os.environ['AZURE_CLIENT_ID']
az_appkey=os.environ['AZURE_CLIENT_SECRET']

# INSTANTIATE SDK CLIENT INSTANCES
sub_client = SubscriptionClient(credentials)

# Connect to each subscription in turn and list all VMs, Functions and Azure SQL servers, collecting CloudGuard billable asset counts
def run_sizer():
    total_number_sql_servers = 0
    total_number_vms = 0
    total_number_functions = 0
    total_stg_used = 0

    stg_time_calc = datetime.datetime.now() - datetime.timedelta(minutes=60)
    stg_time_start = str(stg_time_calc).replace('+00:00','Z')
    stg_time_end = datetime.datetime.now().replace(microsecond=0).isoformat() 
    stg_timespan = stg_time_start + "/" + stg_time_end
    stg_interval = "PT1H"
    stg_metric = "UsedCapacity"

    try:
        for sub in sub_client.subscriptions.list():
            print("\n"),
            print(Fore.CYAN + "================================================================================================")
            print(Fore.WHITE + 'Subscription found:', sub.subscription_id, sub.display_name)
            print(Fore.CYAN + "================================================================================================")

            resource_client = ResourceManagementClient(credentials, sub.subscription_id)
            resource_client.providers.register('Microsoft.Sql')
            sql_client = SqlManagementClient(credentials, sub.subscription_id)
            compute_client = ComputeManagementClient(credentials, sub.subscription_id) 
            web_client = WebSiteManagementClient(credentials, sub.subscription_id)

            storage_client = StorageManagementClient(credentials, sub.subscription_id)
            mgmt_client = MonitorManagementClient(credentials, sub.subscription_id)

            sub_total_number_sql_servers = 0
            sub_total_number_vms = 0
            sub_total_number_functions = 0
            sub_total_number_stgaccts = 0
            rg_stg_used = 0

            print(Fore.WHITE + "================================================================================================")
            print(Fore.YELLOW + "{:20} {:20} {:20}".format("SQL Server Name", "||","Azure Region",))
            print(Fore.WHITE + "================================================================================================")

            for item in sql_client.servers.list():
                print("{:20} {:20} {:20}".format(item.name,"||",item.location))
                sub_total_number_sql_servers = sub_total_number_sql_servers + 1

            print("\n")
            print(Fore.WHITE + "================================================================================================")
            print(Fore.YELLOW + "{:20} {:20} {:20} {:20} {:20}".format("Virtual machine name","||","Instance Size","||","Azure Region"))
            print(Fore.WHITE + "================================================================================================")

            for vm in compute_client.virtual_machines.list_all():    
                print("{:20} {:20} {:20} {:20} {:20}".format(vm.name,"||",vm.hardware_profile.vm_size,"||",vm.location))
                if vm.hardware_profile.vm_size not in ("Standard_A0","Standard_D0","Basic_A0","Basic_D0"):
                    sub_total_number_vms = sub_total_number_vms + 1

            print("\n")
            print(Fore.WHITE + "================================================================================================")
            print(Fore.YELLOW + "{:20} {:20} {:20}".format("Function name","||","Azure Region"))
            print(Fore.WHITE + "================================================================================================")

            for resource_group in resource_client.resource_groups.list():
                rg_name = resource_group.name
                apps_list = web_client.web_apps.list_by_resource_group(rg_name)
                for a in apps_list:
                    appkind = a.kind
                    if "functionapp" in appkind:
                        sub_total_number_functions += 1
                        print("{:20} {:20} {:20}".format(a.name,"||", a.location))

                stg_list = storage_client.storage_accounts.list_by_resource_group(rg_name)
                
                for b in stg_list:
                    stgacct = b.id
                    stgacctname = b.name
                    sub_total_number_stgaccts += 1
                    stg_used_capacity = mgmt_client.metrics.list(stgacct,stg_timespan,stg_interval,stg_metric)
                    stg_capacity_dict = (stg_used_capacity.as_dict())
                    stg_capacity_str = json.dumps(stg_capacity_dict)
                    stg_capacity_json = json.loads(stg_capacity_str)
                    stg_used_value = stg_capacity_json['value'][0]['timeseries'][0]['data'][0]['average']
                    print("\n")
                    print("Storage Account", stgacctname," Used Capacity in bytes:",stg_used_value)
                    rg_stg_used = rg_stg_used + float(stg_used_value)/1024/1024

            total_stg_used = total_stg_used + rg_stg_used
            total_number_sql_servers = total_number_sql_servers + sub_total_number_sql_servers
            total_number_vms = total_number_vms + sub_total_number_vms
            total_number_functions = total_number_functions + sub_total_number_functions

            print("\n")
            print("Total number of billable SQL Servers in subscription", sub.display_name,":",sub_total_number_sql_servers)
            print("Total number of billable virtual machines in subscription", sub.display_name,":",sub_total_number_vms)
            print("Total number of billable functions in subscription", sub.display_name, ":",sub_total_number_functions)
            print("Total log storage used in subscription", sub.display_name, ": {:.2f}".format(total_stg_used)," MB")
    except HttpResponseError as e:
        print(e)
    print("\n")
    print(Fore.GREEN + "================================================================================================")
    print("CloudGuard Azure Sizer - Report Summary")
    print("================================================================================================")
    print("\n")
    print("Total number of billable SQL Servers in Azure AD tenant", az_tenant,":",total_number_sql_servers)
    print("Total number of billable virtual machines in Azure AD tenant", az_tenant,":",total_number_vms)
    print("Total number of billable functions in Azure AD tenant", az_tenant,":",total_number_functions )
    print("\n")
    total_number_functions_licenses = total_number_functions //6
    print("Total number of CloudGuard billable assets licenses is :", total_number_sql_servers + total_number_vms + total_number_functions_licenses)
    print
if __name__ == "__main__":
    run_sizer()