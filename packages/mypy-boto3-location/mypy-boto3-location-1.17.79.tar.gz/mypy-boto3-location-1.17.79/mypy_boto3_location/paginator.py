"""
Type annotations for location service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_location import LocationServiceClient
    from mypy_boto3_location.paginator import (
        GetDevicePositionHistoryPaginator,
        ListGeofenceCollectionsPaginator,
        ListGeofencesPaginator,
        ListMapsPaginator,
        ListPlaceIndexesPaginator,
        ListTrackerConsumersPaginator,
        ListTrackersPaginator,
    )

    client: LocationServiceClient = boto3.client("location")

    get_device_position_history_paginator: GetDevicePositionHistoryPaginator = client.get_paginator("get_device_position_history")
    list_geofence_collections_paginator: ListGeofenceCollectionsPaginator = client.get_paginator("list_geofence_collections")
    list_geofences_paginator: ListGeofencesPaginator = client.get_paginator("list_geofences")
    list_maps_paginator: ListMapsPaginator = client.get_paginator("list_maps")
    list_place_indexes_paginator: ListPlaceIndexesPaginator = client.get_paginator("list_place_indexes")
    list_tracker_consumers_paginator: ListTrackerConsumersPaginator = client.get_paginator("list_tracker_consumers")
    list_trackers_paginator: ListTrackersPaginator = client.get_paginator("list_trackers")
    ```
"""
from datetime import datetime
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    GetDevicePositionHistoryResponseTypeDef,
    ListGeofenceCollectionsResponseTypeDef,
    ListGeofencesResponseTypeDef,
    ListMapsResponseTypeDef,
    ListPlaceIndexesResponseTypeDef,
    ListTrackerConsumersResponseTypeDef,
    ListTrackersResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetDevicePositionHistoryPaginator",
    "ListGeofenceCollectionsPaginator",
    "ListGeofencesPaginator",
    "ListMapsPaginator",
    "ListPlaceIndexesPaginator",
    "ListTrackerConsumersPaginator",
    "ListTrackersPaginator",
)


class GetDevicePositionHistoryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.GetDevicePositionHistory)[Show boto3-stubs documentation](./paginators.md#getdevicepositionhistorypaginator)
    """

    def paginate(
        self,
        DeviceId: str,
        TrackerName: str,
        EndTimeExclusive: datetime = None,
        StartTimeInclusive: datetime = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[GetDevicePositionHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.GetDevicePositionHistory.paginate)
        [Show boto3-stubs documentation](./paginators.md#getdevicepositionhistorypaginator)
        """


class ListGeofenceCollectionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.ListGeofenceCollections)[Show boto3-stubs documentation](./paginators.md#listgeofencecollectionspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListGeofenceCollectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.ListGeofenceCollections.paginate)
        [Show boto3-stubs documentation](./paginators.md#listgeofencecollectionspaginator)
        """


class ListGeofencesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.ListGeofences)[Show boto3-stubs documentation](./paginators.md#listgeofencespaginator)
    """

    def paginate(
        self, CollectionName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListGeofencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.ListGeofences.paginate)
        [Show boto3-stubs documentation](./paginators.md#listgeofencespaginator)
        """


class ListMapsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.ListMaps)[Show boto3-stubs documentation](./paginators.md#listmapspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListMapsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.ListMaps.paginate)
        [Show boto3-stubs documentation](./paginators.md#listmapspaginator)
        """


class ListPlaceIndexesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.ListPlaceIndexes)[Show boto3-stubs documentation](./paginators.md#listplaceindexespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPlaceIndexesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.ListPlaceIndexes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listplaceindexespaginator)
        """


class ListTrackerConsumersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.ListTrackerConsumers)[Show boto3-stubs documentation](./paginators.md#listtrackerconsumerspaginator)
    """

    def paginate(
        self, TrackerName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTrackerConsumersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.ListTrackerConsumers.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtrackerconsumerspaginator)
        """


class ListTrackersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.ListTrackers)[Show boto3-stubs documentation](./paginators.md#listtrackerspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTrackersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/location.html#LocationService.Paginator.ListTrackers.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtrackerspaginator)
        """
