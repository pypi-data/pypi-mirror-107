"""
Type annotations for ivs service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_ivs import IVSClient
    from mypy_boto3_ivs.paginator import (
        ListChannelsPaginator,
        ListPlaybackKeyPairsPaginator,
        ListRecordingConfigurationsPaginator,
        ListStreamKeysPaginator,
        ListStreamsPaginator,
    )

    client: IVSClient = boto3.client("ivs")

    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_playback_key_pairs_paginator: ListPlaybackKeyPairsPaginator = client.get_paginator("list_playback_key_pairs")
    list_recording_configurations_paginator: ListRecordingConfigurationsPaginator = client.get_paginator("list_recording_configurations")
    list_stream_keys_paginator: ListStreamKeysPaginator = client.get_paginator("list_stream_keys")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListChannelsResponseTypeDef,
    ListPlaybackKeyPairsResponseTypeDef,
    ListRecordingConfigurationsResponseTypeDef,
    ListStreamKeysResponseTypeDef,
    ListStreamsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListChannelsPaginator",
    "ListPlaybackKeyPairsPaginator",
    "ListRecordingConfigurationsPaginator",
    "ListStreamKeysPaginator",
    "ListStreamsPaginator",
)


class ListChannelsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ivs.html#IVS.Paginator.ListChannels)[Show boto3-stubs documentation](./paginators.md#listchannelspaginator)
    """

    def paginate(
        self,
        filterByName: str = None,
        filterByRecordingConfigurationArn: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ivs.html#IVS.Paginator.ListChannels.paginate)
        [Show boto3-stubs documentation](./paginators.md#listchannelspaginator)
        """


class ListPlaybackKeyPairsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ivs.html#IVS.Paginator.ListPlaybackKeyPairs)[Show boto3-stubs documentation](./paginators.md#listplaybackkeypairspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPlaybackKeyPairsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ivs.html#IVS.Paginator.ListPlaybackKeyPairs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listplaybackkeypairspaginator)
        """


class ListRecordingConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ivs.html#IVS.Paginator.ListRecordingConfigurations)[Show boto3-stubs documentation](./paginators.md#listrecordingconfigurationspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListRecordingConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ivs.html#IVS.Paginator.ListRecordingConfigurations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listrecordingconfigurationspaginator)
        """


class ListStreamKeysPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ivs.html#IVS.Paginator.ListStreamKeys)[Show boto3-stubs documentation](./paginators.md#liststreamkeyspaginator)
    """

    def paginate(
        self, channelArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListStreamKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ivs.html#IVS.Paginator.ListStreamKeys.paginate)
        [Show boto3-stubs documentation](./paginators.md#liststreamkeyspaginator)
        """


class ListStreamsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ivs.html#IVS.Paginator.ListStreams)[Show boto3-stubs documentation](./paginators.md#liststreamspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ivs.html#IVS.Paginator.ListStreams.paginate)
        [Show boto3-stubs documentation](./paginators.md#liststreamspaginator)
        """
