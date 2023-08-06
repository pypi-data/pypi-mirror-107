"""
Type annotations for location service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_location.literals import BatchItemErrorCodeType

    data: BatchItemErrorCodeType = "AccessDeniedError"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "BatchItemErrorCodeType",
    "GetDevicePositionHistoryPaginatorName",
    "IntendedUseType",
    "ListGeofenceCollectionsPaginatorName",
    "ListGeofencesPaginatorName",
    "ListMapsPaginatorName",
    "ListPlaceIndexesPaginatorName",
    "ListTrackerConsumersPaginatorName",
    "ListTrackersPaginatorName",
    "PricingPlanType",
)

BatchItemErrorCodeType = Literal[
    "AccessDeniedError",
    "ConflictError",
    "InternalServerError",
    "ResourceNotFoundError",
    "ThrottlingError",
    "ValidationError",
]
GetDevicePositionHistoryPaginatorName = Literal["get_device_position_history"]
IntendedUseType = Literal["SingleUse", "Storage"]
ListGeofenceCollectionsPaginatorName = Literal["list_geofence_collections"]
ListGeofencesPaginatorName = Literal["list_geofences"]
ListMapsPaginatorName = Literal["list_maps"]
ListPlaceIndexesPaginatorName = Literal["list_place_indexes"]
ListTrackerConsumersPaginatorName = Literal["list_tracker_consumers"]
ListTrackersPaginatorName = Literal["list_trackers"]
PricingPlanType = Literal["MobileAssetManagement", "MobileAssetTracking", "RequestBasedUsage"]
