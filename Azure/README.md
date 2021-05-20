# CloudGuard-CSPM-Calculator for Azure

## Todo

John - will get network watch flow-log details from SDK
Mark - will get storage details from SDK

## John
- Get network watcher nsg group details

```
az network watcher flow-log list --location westus2
```

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
