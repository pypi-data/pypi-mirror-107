# UsageMetric

A usage metrics for a given resource. A metric contains one or more measurements Provisioned measurements pertain to the set of created resources in the org specified by org_id Active metrics is the set of resources currently deemed active. Each resource has a different algorithm for determining if the usage metric is active or not. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of the Usage | [optional] 
**org_id** | **str** | The unique id of the Organisation to which this record applies.  | [optional] 
**provisioned** | [**UsageMeasurement**](UsageMeasurement.md) |  | [optional] 
**active** | [**UsageMeasurement**](UsageMeasurement.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


