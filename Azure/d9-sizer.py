# This script logs into Azure AD and iterates through subscriptions to onboard them into CloudGuard
# Feedback to chrisbe@checkpoint.com or open an issue on https://github.com/chrisbeckett/d9-azure-sizer/issues

# To run the script, you will need to set environment variables for AZURE_CLIENT_ID, AZURE_CLIENT_SECRET and AZURE_TENANT_ID

# Import required libraries
import os
import sys
import logging
import datetime
import json
import pip

from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.subscription.operations import SubscriptionsOperations
from msrestazure.azure_exceptions import CloudError
from azure.mgmt.compute import ComputeManagementClient
from colorama import Fore, init
from azure.mgmt.web import WebSiteManagementClient
from azure.core.exceptions import HttpResponseError

from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobServiceClient
from azure.identity import AzureCliCredential

init()

try:
    if 'AZURE_TENANT_ID' in os.environ and 'AZURE_CLIENT_ID' in os.environ and 'AZURE_CLIENT_SECRET' in os.environ:
        # Set Azure AD credentials from the environment variables

        # Read in required environment variables
        az_tenant=os.environ['AZURE_TENANT_ID']
        az_appid=os.environ['AZURE_CLIENT_ID']
        az_appkey=os.environ['AZURE_CLIENT_SECRET']

        credentials = ClientSecretCredential(
            client_id=os.environ['AZURE_CLIENT_ID'],
            client_secret=os.environ['AZURE_CLIENT_SECRET'],
            tenant_id=os.environ['AZURE_TENANT_ID']
         )
    else:
        print("\nThe Azure AD tenant ID, client id, and client secrent are not defined in environment variables\n")
        print("Using a service principle account with full access to all subscriptions is recommended\n")
        print("Trying CLI login\n")
          
        try:
            credentials = AzureCliCredential()
        except:
            print("Not logged in, please login with az login or set ENV variable")
            sys.exit(0)
except:
    print("Unable to get connected to Azure")
    sys.exit(0)


# INSTANTIATE SDK CLIENT INSTANCES
sub_client = SubscriptionClient(credentials)


# Connect to each subscription in turn and list all VMs, Functions and Azure SQL servers, collecting CloudGuard billable asset counts
def run_sizer():
    total_number_sql_servers = 0
    total_number_vms = 0
    total_number_functions = 0
    total_flow_stg_used = 0

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
            network_client = NetworkManagementClient(credentials, sub.subscription_id)

            sub_total_number_sql_servers = 0
            sub_total_number_vms = 0
            sub_total_number_functions = 0
            sub_stg_acct_used = 0
            sub_flow_stg_used = 0

            print(Fore.WHITE + "================================================================================================")
            print(Fore.YELLOW + "{:25} {:20} {:20}".format("SQL Server Name", "||","Azure Region",))
            print(Fore.WHITE + "================================================================================================")

            for item in sql_client.servers.list():
                print("{:25} {:20} {:20}".format(item.name,"||",item.location))
                sub_total_number_sql_servers = sub_total_number_sql_servers + 1

            print("\n")
            print(Fore.WHITE + "================================================================================================")
            print(Fore.YELLOW + "{:25} {:20} {:20} {:20} {:20}".format("VM name","||","Instance Size","||","Azure Region"))
            print(Fore.WHITE + "================================================================================================")

            for vm in compute_client.virtual_machines.list_all():    
                print("{:25} {:20} {:20} {:20} {:20}".format(vm.name,"||",vm.hardware_profile.vm_size,"||",vm.location))
                if vm.hardware_profile.vm_size not in ("Standard_A0","Standard_D0","Basic_A0","Basic_D0"):
                    sub_total_number_vms = sub_total_number_vms + 1

            print("\n")
            print(Fore.WHITE + "================================================================================================")
            print(Fore.YELLOW + "{:25} {:20} {:20}".format("Function name","||","Azure Region"))
            print(Fore.WHITE + "================================================================================================")

            for resource_group in resource_client.resource_groups.list():
                rg_name = resource_group.name
                apps_list = web_client.web_apps.list_by_resource_group(rg_name)
                for a in apps_list:
                    appkind = a.kind
                    if "functionapp" in appkind:
                        sub_total_number_functions += 1
                        print("{:25} {:20} {:20}".format(a.name,"||", a.location))

            print("\n")
            #print(Fore.WHITE + "================================================================================================")
            #print(Fore.YELLOW + "{:25} {:20} {:20}".format("Storage Account name","||","Used Size in Bytes"))
            #print(Fore.WHITE + "================================================================================================")
            # Leaving this in for now when we might capture storage account logs
            #for resource_group in resource_client.resource_groups.list():
            #    rg_name = resource_group.name
                #stg_list = storage_client.storage_accounts.list_by_resource_group(rg_name)
                #for b in stg_list:
                #    try: 
                #        stgacct = b.id
                #        stgacctname = b.name
                #        stg_used_capacity = mgmt_client.metrics.list(stgacct,stg_timespan,stg_interval,stg_metric)
                #        stg_capacity_dict = (stg_used_capacity.as_dict())
                #        stg_capacity_str = json.dumps(stg_capacity_dict)
                #        stg_capacity_json = json.loads(stg_capacity_str)
                #        stg_used_value = stg_capacity_json['value'][0]['timeseries'][0]['data'][0]['average']
                #    except Exception as g:
                #        print(g)
                #        print(stgacctname,"Is empty")
                #    else:
                #        print("{:25} {:20} {:20}".format(stgacctname,"||", stg_used_value))
                #        blob_string = "https://" + stgacctname + ".blob.core.windows.net/"
                #        blob_service_client = BlobServiceClient(blob_string,credentials)
                #        all_containers = blob_service_client.list_containers(include_metadata=True)
                #        print("   Containers in this storage account are:")
                #        for container in all_containers:
                #            print("     ",container['name'])
                #        sub_stg_acct_used = sub_stg_acct_used + float(stg_used_value)/1024/1024


            # John
            print(Fore.WHITE + "================================================================================================")
            print(Fore.YELLOW + "{:25} {:20} {:20}".format("Network Watchers -> Flow Logs -> Stg Acct","||","Used Size in Bytes"))
            print(Fore.WHITE + "================================================================================================")
            for network_watcher in network_client.network_watchers.list_all():
                flow_log_list = network_client.flow_logs.list(
                    "NetworkWatcherRG",
                    network_watcher.name
                    )
                for flowlog in flow_log_list:
                    try: 
                        stgacct = flowlog.storage_id
                        stgacctlist = stgacct.rsplit("/",1)
                        stgacctname = stgacctlist[-1]
                        flowlogname = flowlog.name
                        stg_used_capacity = mgmt_client.metrics.list(stgacct,stg_timespan,stg_interval,stg_metric)
                        stg_capacity_dict = (stg_used_capacity.as_dict())
                        stg_capacity_str = json.dumps(stg_capacity_dict)
                        stg_capacity_json = json.loads(stg_capacity_str)
                        stg_used_value = stg_capacity_json['value'][0]['timeseries'][0]['data'][0]['average']
                        print("{:25} {:20} {:20}".format(flowlogname,"||", stg_used_value))
                        print("  The storage account for this flowlog is: ", stgacctname)
                        blob_string = "https://" + stgacctname + ".blob.core.windows.net/"
                        blob_service_client = BlobServiceClient(blob_string,credentials)
                        all_containers = blob_service_client.list_containers(include_metadata=True)
                        sub_flow_stg_used = sub_flow_stg_used + float(stg_used_value)/1024/1024
                        for container in all_containers:
                            if container['name'] != "insights-logs-networksecuritygroupflowevent":
                                print("WARNING, calculation may be off because of this container:",container['name'])
                    except Exception as f: 
                        notauthorized = "AuthorizationPermissionMismatch"
                        if notauthorized in f.message:
                            print("Insufficient permissions to validate all of the Storage Account")
                            pass

            total_number_sql_servers = total_number_sql_servers + sub_total_number_sql_servers
            total_number_vms = total_number_vms + sub_total_number_vms
            total_number_functions = total_number_functions + sub_total_number_functions
            total_flow_stg_used = total_flow_stg_used + sub_flow_stg_used

            print("\n")
            print("Total number of billable SQL Servers in subscription", sub.display_name,":",sub_total_number_sql_servers)
            print("Total number of billable virtual machines in subscription", sub.display_name,":",sub_total_number_vms)
            print("Total number of billable functions in subscription", sub.display_name, ":",sub_total_number_functions)
            print("Total estimated flowlog storage used in subscription", sub.display_name, ": {:.2f}".format(sub_flow_stg_used)," MB")
    except HttpResponseError as e:
        notauthorized = "AuthorizationPermissionMismatch"
        if notauthorized in e.message:
            print("All subscriptions are not included in this calculation")
            pass
    print("\n")
    print(Fore.GREEN + "================================================================================================")
    print("CloudGuard Azure Sizer - Report Summary")
    print("================================================================================================")
    print("\n")
    print("Total number of billable SQL Servers in Azure AD tenant:",total_number_sql_servers)
    print("Total number of billable virtual machines in Azure AD tenant:",total_number_vms)
    print("Total number of billable functions in Azure AD tenant:",total_number_functions )
    print("Total estimated flowlog storage used in Azure AD tenant : {:.2f}".format(total_flow_stg_used)," MB")
    print("\n")
    total_number_functions_licenses = total_number_functions //6
    print("Total number of CloudGuard billable assets licenses is :", total_number_sql_servers + total_number_vms + total_number_functions_licenses)
    print
if __name__ == "__main__":
    run_sizer()
