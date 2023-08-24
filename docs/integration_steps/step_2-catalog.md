# Cloud Catalog

A catalog is a CSV file under [SkyPilot Catalogs](https://github.com/skypilot-org/skypilot-catalog)

| Field | Type | Description |
| ----- | ---- | ----------- |
| `InstanceType` | string | The type of instance. |
| `vCPUs` | float | The number of virtual CPUs. |
| `MemoryGiB` | float | The amount of memory in GB. |
| `AcceleratorName` | string | The name of accelerators (GPU/TPU). |
| `AcceleratorCount` | float | The number of accelerators (GPU/TPU). |
| `GPUInfo` | string | The human readable information of the GPU (not used in code). |
| `Region` | string | The region of the resource. |
| `AvailabilityZone` | string | The availability zone of the resource (can be empty if not supported in the cloud). |
| `Price` | float | The price of the resource. |
| `SpotPrice` | float | The spot price of the resource. |


## Parsing Catalog
