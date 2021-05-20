# CloudGuard-CSPM-Calculator for Azure

## Todo flow logs

John - will get network watch flow-log details from SDK
Mark - will get storage details from SDK

## Todo flow logs

User activity logs (Not started yet)

## John
- Get network watcher nsg group details

Az command
```
az network watcher flow-log list --location westus2
```

Python
```
    network_watcher_list = network_client.network_watchers.list_all()
    for network_watcher in network_watcher_list:
        print(network_watcher)

    network_security_groups_list = network_client.network_security_groups.list_all()
    for network_security_groups in network_security_groups_list:
        print(network_security_groups)
```

    (mytestenv) mymac:watcher john$ python3 manage_network_watcher.py
    {'additional_properties': {}, 'id': '/subscriptions/5fca0708-dbdf-4211-869b-b9eecde28279/resourceGroups/guo-win10-test-rg/providers/Microsoft.Network/networkSecurityGroups/guo-win10-test-nsg', 'name': 'guo-win10-test-nsg', 'type': 'Microsoft.Network/networkSecurityGroups', 'location': 'westus2', 'tags': None, 'etag': 'W/"d50d9816-4526-4fd6-ab28-1b8c5a5f25f3"', 'security_rules': [<azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863040>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863160>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863130>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8631c0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8631f0>], 'default_security_rules': [<azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863220>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863250>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863280>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8632b0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8632e0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863310>], 'network_interfaces': [<azure.mgmt.network.v2020_06_01.models._models_py3.NetworkInterface object at 0x10c863190>], 'subnets': None, 'flow_logs': [<azure.mgmt.network.v2020_06_01.models._models_py3.FlowLog object at 0x10c8633d0>], 'resource_guid': '9a8fffd6-2180-4e9d-8355-ca5164ef6402', 'provisioning_state': 'Succeeded'}

    {'additional_properties': {}, 'id': '/subscriptions/5fca0708-dbdf-4211-869b-b9eecde28279/resourceGroups/guor81mgmt-rg/providers/Microsoft.Network/networkSecurityGroups/guor81mgmt-nsg', 'name': 'guor81mgmt-nsg', 'type': 'Microsoft.Network/networkSecurityGroups', 'location': 'westus2', 'tags': {'provider': '30DE18BC-F9F6-4F22-9D30-54B8E74CFD5F'}, 'etag': 'W/"e0740a01-a65b-4d2f-ba5a-344fdea0eea6"', 'security_rules': [<azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8633a0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863400>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863370>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863460>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863490>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8634c0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8634f0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863520>], 'default_security_rules': [<azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863550>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863580>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8635b0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8635e0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863610>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863640>], 'network_interfaces': [<azure.mgmt.network.v2020_06_01.models._models_py3.NetworkInterface object at 0x10c863430>], 'subnets': None, 'flow_logs': [<azure.mgmt.network.v2020_06_01.models._models_py3.FlowLog object at 0x10c863700>], 'resource_guid': 'bde5eb1e-e095-4028-8218-49c74984ea90', 'provisioning_state': 'Succeeded'}
    
    {'additional_properties': {}, 'id': '/subscriptions/5fca0708-dbdf-4211-869b-b9eecde28279/resourceGroups/ubuntu-server-rg/providers/Microsoft.Network/networkSecurityGroups/ubuntuserver-nsg', 'name': 'ubuntuserver-nsg', 'type': 'Microsoft.Network/networkSecurityGroups', 'location': 'westus2', 'tags': None, 'etag': 'W/"e9c1f40b-09b9-43bb-81fd-e36bfedfa8ae"', 'security_rules': [<azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8636d0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863730>], 'default_security_rules': [<azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8636a0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863790>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8637c0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8637f0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863820>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863850>], 'network_interfaces': [<azure.mgmt.network.v2020_06_01.models._models_py3.NetworkInterface object at 0x10c863760>], 'subnets': None, 'flow_logs': [<azure.mgmt.network.v2020_06_01.models._models_py3.FlowLog object at 0x10c863910>], 'resource_guid': '2d176eb0-426c-4d0f-8c57-42f6ec209555', 'provisioning_state': 'Succeeded'}
    
    {'additional_properties': {}, 'id': '/subscriptions/5fca0708-dbdf-4211-869b-b9eecde28279/resourceGroups/vnet_10.200.0.0-rg/providers/Microsoft.Network/networkSecurityGroups/guo-any-any', 'name': 'guo-any-any', 'type': 'Microsoft.Network/networkSecurityGroups', 'location': 'westus2', 'tags': {}, 'etag': 'W/"8d401cee-e6bd-48b4-acef-936774846897"', 'security_rules': [<azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8638e0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863940>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8638b0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8639a0>], 'default_security_rules': [<azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c8639d0>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863a00>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863a30>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863a60>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863a90>, <azure.mgmt.network.v2020_06_01.models._models_py3.SecurityRule object at 0x10c863ac0>], 'network_interfaces': None, 'subnets': [<azure.mgmt.network.v2020_06_01.models._models_py3.Subnet object at 0x10c863970>], 'flow_logs': [<azure.mgmt.network.v2020_06_01.models._models_py3.FlowLog object at 0x10c863b80>], 'resource_guid': '63d30831-b91e-46d5-9bde-34ca9da2f3f2', 'provisioning_state': 'Succeeded'}
    
    {'additional_properties': {}, 'id': '/subscriptions/5fca0708-dbdf-4211-869b-b9eecde28279/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkWatchers/NetworkWatcher_westus2', 'name': 'NetworkWatcher_westus2', 'type': 'Microsoft.Network/networkWatchers', 'location': 'westus2', 'tags': None, 'etag': 'W/"c9910812-1719-4463-95de-667e77ca33e1"', 'provisioning_state': 'Succeeded'}


## Mark
- Get data in json format
```
az monitor metrics list --resource "/subscriptions/0c463575-043a-4ee1-8f71-ba14325e2f0d/resourceGroups/k8s-testing/providers/Microsoft.Storage/storageAccounts/mnstgacct"  --metric "UsedCapacity" --interval PT1H
```

## References

- MS Python SDK detail

https://github.com/Azure/azure-sdk-for-python
https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-overview

- MS Python SDK reference

https://docs.microsoft.com/en-us/azure/developer/python/sdk-library-api-reference

https://docs.microsoft.com/en-us/python/api/?view=azure-python

https://docs.microsoft.com/en-us/azure/developer/python/sdk-library-api-reference


    - watcher 
    
    https://docs.microsoft.com/en-us/python/api/azure-mgmt-network/azure.mgmt.network.v2019_04_01.operations.networkwatchersoperations?view=azure-python#list-all---kwargs-


- Samples of Azure Python SDK

https://github.com/Azure-Samples/azure-samples-python-management/tree/master/samples

- Get NSG group

https://github.com/erjosito/get_nsg_logs/blob/master/get_nsg_logs.py
