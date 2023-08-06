"""
Type annotations for location service type definitions.

[Open documentation](./type_defs.md)

Usage::

    ```python
    from mypy_boto3_location.type_defs import BatchDeleteGeofenceErrorTypeDef

    data: BatchDeleteGeofenceErrorTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, List, Union

from .literals import BatchItemErrorCodeType, IntendedUseType, PricingPlanType

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BatchDeleteGeofenceErrorTypeDef",
    "BatchDeleteGeofenceResponseTypeDef",
    "BatchEvaluateGeofencesErrorTypeDef",
    "BatchEvaluateGeofencesResponseTypeDef",
    "BatchGetDevicePositionErrorTypeDef",
    "BatchGetDevicePositionResponseTypeDef",
    "BatchItemErrorTypeDef",
    "BatchPutGeofenceErrorTypeDef",
    "BatchPutGeofenceRequestEntryTypeDef",
    "BatchPutGeofenceResponseTypeDef",
    "BatchPutGeofenceSuccessTypeDef",
    "BatchUpdateDevicePositionErrorTypeDef",
    "BatchUpdateDevicePositionResponseTypeDef",
    "CreateGeofenceCollectionResponseTypeDef",
    "CreateMapResponseTypeDef",
    "CreatePlaceIndexResponseTypeDef",
    "CreateTrackerResponseTypeDef",
    "DataSourceConfigurationTypeDef",
    "DescribeGeofenceCollectionResponseTypeDef",
    "DescribeMapResponseTypeDef",
    "DescribePlaceIndexResponseTypeDef",
    "DescribeTrackerResponseTypeDef",
    "DevicePositionTypeDef",
    "DevicePositionUpdateTypeDef",
    "GeofenceGeometryTypeDef",
    "GetDevicePositionHistoryResponseTypeDef",
    "GetDevicePositionResponseTypeDef",
    "GetGeofenceResponseTypeDef",
    "GetMapGlyphsResponseTypeDef",
    "GetMapSpritesResponseTypeDef",
    "GetMapStyleDescriptorResponseTypeDef",
    "GetMapTileResponseTypeDef",
    "ListGeofenceCollectionsResponseEntryTypeDef",
    "ListGeofenceCollectionsResponseTypeDef",
    "ListGeofenceResponseEntryTypeDef",
    "ListGeofencesResponseTypeDef",
    "ListMapsResponseEntryTypeDef",
    "ListMapsResponseTypeDef",
    "ListPlaceIndexesResponseEntryTypeDef",
    "ListPlaceIndexesResponseTypeDef",
    "ListTrackerConsumersResponseTypeDef",
    "ListTrackersResponseEntryTypeDef",
    "ListTrackersResponseTypeDef",
    "MapConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PlaceGeometryTypeDef",
    "PlaceTypeDef",
    "PutGeofenceResponseTypeDef",
    "SearchForPositionResultTypeDef",
    "SearchForTextResultTypeDef",
    "SearchPlaceIndexForPositionResponseTypeDef",
    "SearchPlaceIndexForPositionSummaryTypeDef",
    "SearchPlaceIndexForTextResponseTypeDef",
    "SearchPlaceIndexForTextSummaryTypeDef",
)

BatchDeleteGeofenceErrorTypeDef = TypedDict(
    "BatchDeleteGeofenceErrorTypeDef",
    {
        "Error": "BatchItemErrorTypeDef",
        "GeofenceId": str,
    },
)

BatchDeleteGeofenceResponseTypeDef = TypedDict(
    "BatchDeleteGeofenceResponseTypeDef",
    {
        "Errors": List["BatchDeleteGeofenceErrorTypeDef"],
    },
)

BatchEvaluateGeofencesErrorTypeDef = TypedDict(
    "BatchEvaluateGeofencesErrorTypeDef",
    {
        "DeviceId": str,
        "Error": "BatchItemErrorTypeDef",
        "SampleTime": datetime,
    },
)

BatchEvaluateGeofencesResponseTypeDef = TypedDict(
    "BatchEvaluateGeofencesResponseTypeDef",
    {
        "Errors": List["BatchEvaluateGeofencesErrorTypeDef"],
    },
)

BatchGetDevicePositionErrorTypeDef = TypedDict(
    "BatchGetDevicePositionErrorTypeDef",
    {
        "DeviceId": str,
        "Error": "BatchItemErrorTypeDef",
    },
)

BatchGetDevicePositionResponseTypeDef = TypedDict(
    "BatchGetDevicePositionResponseTypeDef",
    {
        "DevicePositions": List["DevicePositionTypeDef"],
        "Errors": List["BatchGetDevicePositionErrorTypeDef"],
    },
)

BatchItemErrorTypeDef = TypedDict(
    "BatchItemErrorTypeDef",
    {
        "Code": BatchItemErrorCodeType,
        "Message": str,
    },
    total=False,
)

BatchPutGeofenceErrorTypeDef = TypedDict(
    "BatchPutGeofenceErrorTypeDef",
    {
        "Error": "BatchItemErrorTypeDef",
        "GeofenceId": str,
    },
)

BatchPutGeofenceRequestEntryTypeDef = TypedDict(
    "BatchPutGeofenceRequestEntryTypeDef",
    {
        "GeofenceId": str,
        "Geometry": "GeofenceGeometryTypeDef",
    },
)

BatchPutGeofenceResponseTypeDef = TypedDict(
    "BatchPutGeofenceResponseTypeDef",
    {
        "Errors": List["BatchPutGeofenceErrorTypeDef"],
        "Successes": List["BatchPutGeofenceSuccessTypeDef"],
    },
)

BatchPutGeofenceSuccessTypeDef = TypedDict(
    "BatchPutGeofenceSuccessTypeDef",
    {
        "CreateTime": datetime,
        "GeofenceId": str,
        "UpdateTime": datetime,
    },
)

BatchUpdateDevicePositionErrorTypeDef = TypedDict(
    "BatchUpdateDevicePositionErrorTypeDef",
    {
        "DeviceId": str,
        "Error": "BatchItemErrorTypeDef",
        "SampleTime": datetime,
    },
)

BatchUpdateDevicePositionResponseTypeDef = TypedDict(
    "BatchUpdateDevicePositionResponseTypeDef",
    {
        "Errors": List["BatchUpdateDevicePositionErrorTypeDef"],
    },
)

CreateGeofenceCollectionResponseTypeDef = TypedDict(
    "CreateGeofenceCollectionResponseTypeDef",
    {
        "CollectionArn": str,
        "CollectionName": str,
        "CreateTime": datetime,
    },
)

CreateMapResponseTypeDef = TypedDict(
    "CreateMapResponseTypeDef",
    {
        "CreateTime": datetime,
        "MapArn": str,
        "MapName": str,
    },
)

CreatePlaceIndexResponseTypeDef = TypedDict(
    "CreatePlaceIndexResponseTypeDef",
    {
        "CreateTime": datetime,
        "IndexArn": str,
        "IndexName": str,
    },
)

CreateTrackerResponseTypeDef = TypedDict(
    "CreateTrackerResponseTypeDef",
    {
        "CreateTime": datetime,
        "TrackerArn": str,
        "TrackerName": str,
    },
)

DataSourceConfigurationTypeDef = TypedDict(
    "DataSourceConfigurationTypeDef",
    {
        "IntendedUse": IntendedUseType,
    },
    total=False,
)

_RequiredDescribeGeofenceCollectionResponseTypeDef = TypedDict(
    "_RequiredDescribeGeofenceCollectionResponseTypeDef",
    {
        "CollectionArn": str,
        "CollectionName": str,
        "CreateTime": datetime,
        "Description": str,
        "PricingPlan": PricingPlanType,
        "UpdateTime": datetime,
    },
)
_OptionalDescribeGeofenceCollectionResponseTypeDef = TypedDict(
    "_OptionalDescribeGeofenceCollectionResponseTypeDef",
    {
        "PricingPlanDataSource": str,
    },
    total=False,
)


class DescribeGeofenceCollectionResponseTypeDef(
    _RequiredDescribeGeofenceCollectionResponseTypeDef,
    _OptionalDescribeGeofenceCollectionResponseTypeDef,
):
    pass


DescribeMapResponseTypeDef = TypedDict(
    "DescribeMapResponseTypeDef",
    {
        "Configuration": "MapConfigurationTypeDef",
        "CreateTime": datetime,
        "DataSource": str,
        "Description": str,
        "MapArn": str,
        "MapName": str,
        "PricingPlan": PricingPlanType,
        "UpdateTime": datetime,
    },
)

DescribePlaceIndexResponseTypeDef = TypedDict(
    "DescribePlaceIndexResponseTypeDef",
    {
        "CreateTime": datetime,
        "DataSource": str,
        "DataSourceConfiguration": "DataSourceConfigurationTypeDef",
        "Description": str,
        "IndexArn": str,
        "IndexName": str,
        "PricingPlan": PricingPlanType,
        "UpdateTime": datetime,
    },
)

_RequiredDescribeTrackerResponseTypeDef = TypedDict(
    "_RequiredDescribeTrackerResponseTypeDef",
    {
        "CreateTime": datetime,
        "Description": str,
        "PricingPlan": PricingPlanType,
        "TrackerArn": str,
        "TrackerName": str,
        "UpdateTime": datetime,
    },
)
_OptionalDescribeTrackerResponseTypeDef = TypedDict(
    "_OptionalDescribeTrackerResponseTypeDef",
    {
        "PricingPlanDataSource": str,
    },
    total=False,
)


class DescribeTrackerResponseTypeDef(
    _RequiredDescribeTrackerResponseTypeDef, _OptionalDescribeTrackerResponseTypeDef
):
    pass


_RequiredDevicePositionTypeDef = TypedDict(
    "_RequiredDevicePositionTypeDef",
    {
        "Position": List[float],
        "ReceivedTime": datetime,
        "SampleTime": datetime,
    },
)
_OptionalDevicePositionTypeDef = TypedDict(
    "_OptionalDevicePositionTypeDef",
    {
        "DeviceId": str,
    },
    total=False,
)


class DevicePositionTypeDef(_RequiredDevicePositionTypeDef, _OptionalDevicePositionTypeDef):
    pass


DevicePositionUpdateTypeDef = TypedDict(
    "DevicePositionUpdateTypeDef",
    {
        "DeviceId": str,
        "Position": List[float],
        "SampleTime": datetime,
    },
)

GeofenceGeometryTypeDef = TypedDict(
    "GeofenceGeometryTypeDef",
    {
        "Polygon": List[List[List[float]]],
    },
    total=False,
)

_RequiredGetDevicePositionHistoryResponseTypeDef = TypedDict(
    "_RequiredGetDevicePositionHistoryResponseTypeDef",
    {
        "DevicePositions": List["DevicePositionTypeDef"],
    },
)
_OptionalGetDevicePositionHistoryResponseTypeDef = TypedDict(
    "_OptionalGetDevicePositionHistoryResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class GetDevicePositionHistoryResponseTypeDef(
    _RequiredGetDevicePositionHistoryResponseTypeDef,
    _OptionalGetDevicePositionHistoryResponseTypeDef,
):
    pass


_RequiredGetDevicePositionResponseTypeDef = TypedDict(
    "_RequiredGetDevicePositionResponseTypeDef",
    {
        "Position": List[float],
        "ReceivedTime": datetime,
        "SampleTime": datetime,
    },
)
_OptionalGetDevicePositionResponseTypeDef = TypedDict(
    "_OptionalGetDevicePositionResponseTypeDef",
    {
        "DeviceId": str,
    },
    total=False,
)


class GetDevicePositionResponseTypeDef(
    _RequiredGetDevicePositionResponseTypeDef, _OptionalGetDevicePositionResponseTypeDef
):
    pass


GetGeofenceResponseTypeDef = TypedDict(
    "GetGeofenceResponseTypeDef",
    {
        "CreateTime": datetime,
        "GeofenceId": str,
        "Geometry": "GeofenceGeometryTypeDef",
        "Status": str,
        "UpdateTime": datetime,
    },
)

GetMapGlyphsResponseTypeDef = TypedDict(
    "GetMapGlyphsResponseTypeDef",
    {
        "Blob": Union[bytes, IO[bytes]],
        "ContentType": str,
    },
    total=False,
)

GetMapSpritesResponseTypeDef = TypedDict(
    "GetMapSpritesResponseTypeDef",
    {
        "Blob": Union[bytes, IO[bytes]],
        "ContentType": str,
    },
    total=False,
)

GetMapStyleDescriptorResponseTypeDef = TypedDict(
    "GetMapStyleDescriptorResponseTypeDef",
    {
        "Blob": Union[bytes, IO[bytes]],
        "ContentType": str,
    },
    total=False,
)

GetMapTileResponseTypeDef = TypedDict(
    "GetMapTileResponseTypeDef",
    {
        "Blob": Union[bytes, IO[bytes]],
        "ContentType": str,
    },
    total=False,
)

_RequiredListGeofenceCollectionsResponseEntryTypeDef = TypedDict(
    "_RequiredListGeofenceCollectionsResponseEntryTypeDef",
    {
        "CollectionName": str,
        "CreateTime": datetime,
        "Description": str,
        "PricingPlan": PricingPlanType,
        "UpdateTime": datetime,
    },
)
_OptionalListGeofenceCollectionsResponseEntryTypeDef = TypedDict(
    "_OptionalListGeofenceCollectionsResponseEntryTypeDef",
    {
        "PricingPlanDataSource": str,
    },
    total=False,
)


class ListGeofenceCollectionsResponseEntryTypeDef(
    _RequiredListGeofenceCollectionsResponseEntryTypeDef,
    _OptionalListGeofenceCollectionsResponseEntryTypeDef,
):
    pass


_RequiredListGeofenceCollectionsResponseTypeDef = TypedDict(
    "_RequiredListGeofenceCollectionsResponseTypeDef",
    {
        "Entries": List["ListGeofenceCollectionsResponseEntryTypeDef"],
    },
)
_OptionalListGeofenceCollectionsResponseTypeDef = TypedDict(
    "_OptionalListGeofenceCollectionsResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListGeofenceCollectionsResponseTypeDef(
    _RequiredListGeofenceCollectionsResponseTypeDef, _OptionalListGeofenceCollectionsResponseTypeDef
):
    pass


ListGeofenceResponseEntryTypeDef = TypedDict(
    "ListGeofenceResponseEntryTypeDef",
    {
        "CreateTime": datetime,
        "GeofenceId": str,
        "Geometry": "GeofenceGeometryTypeDef",
        "Status": str,
        "UpdateTime": datetime,
    },
)

_RequiredListGeofencesResponseTypeDef = TypedDict(
    "_RequiredListGeofencesResponseTypeDef",
    {
        "Entries": List["ListGeofenceResponseEntryTypeDef"],
    },
)
_OptionalListGeofencesResponseTypeDef = TypedDict(
    "_OptionalListGeofencesResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListGeofencesResponseTypeDef(
    _RequiredListGeofencesResponseTypeDef, _OptionalListGeofencesResponseTypeDef
):
    pass


ListMapsResponseEntryTypeDef = TypedDict(
    "ListMapsResponseEntryTypeDef",
    {
        "CreateTime": datetime,
        "DataSource": str,
        "Description": str,
        "MapName": str,
        "PricingPlan": PricingPlanType,
        "UpdateTime": datetime,
    },
)

_RequiredListMapsResponseTypeDef = TypedDict(
    "_RequiredListMapsResponseTypeDef",
    {
        "Entries": List["ListMapsResponseEntryTypeDef"],
    },
)
_OptionalListMapsResponseTypeDef = TypedDict(
    "_OptionalListMapsResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListMapsResponseTypeDef(_RequiredListMapsResponseTypeDef, _OptionalListMapsResponseTypeDef):
    pass


ListPlaceIndexesResponseEntryTypeDef = TypedDict(
    "ListPlaceIndexesResponseEntryTypeDef",
    {
        "CreateTime": datetime,
        "DataSource": str,
        "Description": str,
        "IndexName": str,
        "PricingPlan": PricingPlanType,
        "UpdateTime": datetime,
    },
)

_RequiredListPlaceIndexesResponseTypeDef = TypedDict(
    "_RequiredListPlaceIndexesResponseTypeDef",
    {
        "Entries": List["ListPlaceIndexesResponseEntryTypeDef"],
    },
)
_OptionalListPlaceIndexesResponseTypeDef = TypedDict(
    "_OptionalListPlaceIndexesResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListPlaceIndexesResponseTypeDef(
    _RequiredListPlaceIndexesResponseTypeDef, _OptionalListPlaceIndexesResponseTypeDef
):
    pass


_RequiredListTrackerConsumersResponseTypeDef = TypedDict(
    "_RequiredListTrackerConsumersResponseTypeDef",
    {
        "ConsumerArns": List[str],
    },
)
_OptionalListTrackerConsumersResponseTypeDef = TypedDict(
    "_OptionalListTrackerConsumersResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListTrackerConsumersResponseTypeDef(
    _RequiredListTrackerConsumersResponseTypeDef, _OptionalListTrackerConsumersResponseTypeDef
):
    pass


_RequiredListTrackersResponseEntryTypeDef = TypedDict(
    "_RequiredListTrackersResponseEntryTypeDef",
    {
        "CreateTime": datetime,
        "Description": str,
        "PricingPlan": PricingPlanType,
        "TrackerName": str,
        "UpdateTime": datetime,
    },
)
_OptionalListTrackersResponseEntryTypeDef = TypedDict(
    "_OptionalListTrackersResponseEntryTypeDef",
    {
        "PricingPlanDataSource": str,
    },
    total=False,
)


class ListTrackersResponseEntryTypeDef(
    _RequiredListTrackersResponseEntryTypeDef, _OptionalListTrackersResponseEntryTypeDef
):
    pass


_RequiredListTrackersResponseTypeDef = TypedDict(
    "_RequiredListTrackersResponseTypeDef",
    {
        "Entries": List["ListTrackersResponseEntryTypeDef"],
    },
)
_OptionalListTrackersResponseTypeDef = TypedDict(
    "_OptionalListTrackersResponseTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListTrackersResponseTypeDef(
    _RequiredListTrackersResponseTypeDef, _OptionalListTrackersResponseTypeDef
):
    pass


MapConfigurationTypeDef = TypedDict(
    "MapConfigurationTypeDef",
    {
        "Style": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

PlaceGeometryTypeDef = TypedDict(
    "PlaceGeometryTypeDef",
    {
        "Point": List[float],
    },
    total=False,
)

_RequiredPlaceTypeDef = TypedDict(
    "_RequiredPlaceTypeDef",
    {
        "Geometry": "PlaceGeometryTypeDef",
    },
)
_OptionalPlaceTypeDef = TypedDict(
    "_OptionalPlaceTypeDef",
    {
        "AddressNumber": str,
        "Country": str,
        "Label": str,
        "Municipality": str,
        "Neighborhood": str,
        "PostalCode": str,
        "Region": str,
        "Street": str,
        "SubRegion": str,
    },
    total=False,
)


class PlaceTypeDef(_RequiredPlaceTypeDef, _OptionalPlaceTypeDef):
    pass


PutGeofenceResponseTypeDef = TypedDict(
    "PutGeofenceResponseTypeDef",
    {
        "CreateTime": datetime,
        "GeofenceId": str,
        "UpdateTime": datetime,
    },
)

SearchForPositionResultTypeDef = TypedDict(
    "SearchForPositionResultTypeDef",
    {
        "Place": "PlaceTypeDef",
    },
)

SearchForTextResultTypeDef = TypedDict(
    "SearchForTextResultTypeDef",
    {
        "Place": "PlaceTypeDef",
    },
)

SearchPlaceIndexForPositionResponseTypeDef = TypedDict(
    "SearchPlaceIndexForPositionResponseTypeDef",
    {
        "Results": List["SearchForPositionResultTypeDef"],
        "Summary": "SearchPlaceIndexForPositionSummaryTypeDef",
    },
)

_RequiredSearchPlaceIndexForPositionSummaryTypeDef = TypedDict(
    "_RequiredSearchPlaceIndexForPositionSummaryTypeDef",
    {
        "DataSource": str,
        "Position": List[float],
    },
)
_OptionalSearchPlaceIndexForPositionSummaryTypeDef = TypedDict(
    "_OptionalSearchPlaceIndexForPositionSummaryTypeDef",
    {
        "MaxResults": int,
    },
    total=False,
)


class SearchPlaceIndexForPositionSummaryTypeDef(
    _RequiredSearchPlaceIndexForPositionSummaryTypeDef,
    _OptionalSearchPlaceIndexForPositionSummaryTypeDef,
):
    pass


SearchPlaceIndexForTextResponseTypeDef = TypedDict(
    "SearchPlaceIndexForTextResponseTypeDef",
    {
        "Results": List["SearchForTextResultTypeDef"],
        "Summary": "SearchPlaceIndexForTextSummaryTypeDef",
    },
)

_RequiredSearchPlaceIndexForTextSummaryTypeDef = TypedDict(
    "_RequiredSearchPlaceIndexForTextSummaryTypeDef",
    {
        "DataSource": str,
        "Text": str,
    },
)
_OptionalSearchPlaceIndexForTextSummaryTypeDef = TypedDict(
    "_OptionalSearchPlaceIndexForTextSummaryTypeDef",
    {
        "BiasPosition": List[float],
        "FilterBBox": List[float],
        "FilterCountries": List[str],
        "MaxResults": int,
        "ResultBBox": List[float],
    },
    total=False,
)


class SearchPlaceIndexForTextSummaryTypeDef(
    _RequiredSearchPlaceIndexForTextSummaryTypeDef, _OptionalSearchPlaceIndexForTextSummaryTypeDef
):
    pass
