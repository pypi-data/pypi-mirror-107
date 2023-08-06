# Resource

A resource in the system. A resource represents something with which a user can interact. Users may be granted permission to access a resource. Each resource has a unique permission scheme, which controls how a user may access it when granted the associated role. Resources are hierarchical, meaning that one resource may be a child of another. When a parent resources is deleted, all its children are deleted. A user with a role in a parent resource has the same role in its child resources, and so on, recursively.  Each resource is uniquely identified by `metadata.id`. That identifier matches the identifier for the resource in its specific collection (e.g. /v2/applications, /v1/file_shares, etc) 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**MetadataWithId**](MetadataWithId.md) |  | [optional] 
**spec** | [**ResourceSpec**](ResourceSpec.md) |  | 
**status** | [**ResourceStatus**](ResourceStatus.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


