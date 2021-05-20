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

- Samples of Azure Python SDK

https://github.com/Azure-Samples/azure-samples-python-management/tree/master/samples

- Get NSG group

https://github.com/erjosito/get_nsg_logs/blob/master/get_nsg_logs.py
