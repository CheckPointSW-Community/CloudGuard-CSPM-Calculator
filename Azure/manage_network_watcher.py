# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    NETWORK_WATCHER = "network_watcherxxyyzz"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )


    # Steps


    # List all security group + network watcher

    network_security_groups_list = network_client.network_security_groups.list_all()
    for network_security_groups in network_security_groups_list:
        print(network_security_groups)

    network_watcher_list = network_client.network_watchers.list_all()
    for network_watcher in network_watcher_list:
        print(network_watcher)

    # List network watcher details

        # network_watcher_list = network_client.flow_logs.list.NetworkWatcherRG.guo-any-any-vnet_10.200.0.0-rg-flowlog()
        # for network_watcher in network_watcher_list:
        # print(network_watcher)
        # Need work

    # List storage account details



    ########
    # Testing
    ########
    # # Test resource group example - START
    # group_list = resource_client.resource_groups.list()

    # # Show the groups in formatted output
    # column_width = 40

    # print("Resource Group".ljust(column_width) + "Location")
    # print("-" * (column_width * 2))

    # for group in list(group_list):
    #     print(f"{group.name:<{column_width}}{group.location}")

    # Test resource group example - END     

    # network_watcher_list = network_client.flow_logs.list.NetworkWatcherRG.guo-any-any-vnet_10.200.0.0-rg-flowlog()
    # for network_watcher in network_watcher_list:
    #     print(network_watcher)

    # network_watcher_list = network_client.network_watchers.list_all()
    # for network_watcher in network_watcher_list:
    #     print(network_watcher)

    # network_security_groups_list = network_client.network_security_groups.list_all()
    # for network_security_groups in network_security_groups_list:
    #     print(network_security_groups)

    # List network watchers
    # networkwatcher_list = network_client.network_watchers.list_all()
    # column_width1 = 60
    # print("Network Watchers".ljust(column_width1) + "Location")
    # print("-" * (column_width1 * 2))
    # networkwatcher_list
    # for watcher in list(networkwatcher_list):
    #     print(f"{networkwatchers.name:<{column_width}}{group.location}")

    # print(guo)
    # # Create resource group
    # resource_client.resource_groups.create_or_update(
    #     GROUP_NAME,
    #     {"location": "eastus"}
    # )

    # # Create network watcher
    # network_watcher = network_client.network_watchers.create_or_update(
    #     GROUP_NAME,
    #     NETWORK_WATCHER,
    #     {
    #       "location": "eastus"
    #     }
    # )
    # print("Create network watcher:\n{}".format(network_watcher))

    # # Get network watcher
    # network_watcher = network_client.network_watchers.get(
    #     GROUP_NAME,
    #     NETWORK_WATCHER
    # )
    # print("Get network watcher:\n{}".format(network_watcher))

    # # Update network watcher
    # network_watcher = network_client.network_watchers.update_tags(
    #     GROUP_NAME,
    #     NETWORK_WATCHER,
    #     {
    #       "tags": {
    #         "tag1": "value1",
    #         "tag2": "value2"
    #       }
    #     }
    # )
    # print("Update network watcher:\n{}".format(network_watcher))
    
    # # Delete network watcher
    # network_watcher = network_client.network_watchers.begin_delete(
    #     GROUP_NAME,
    #     NETWORK_WATCHER
    # ).result()
    # print("Delete network watcher.\n")

    # # Delete Group
    # resource_client.resource_groups.begin_delete(
    #     GROUP_NAME
    # ).result()


if __name__ == "__main__":
    main()
