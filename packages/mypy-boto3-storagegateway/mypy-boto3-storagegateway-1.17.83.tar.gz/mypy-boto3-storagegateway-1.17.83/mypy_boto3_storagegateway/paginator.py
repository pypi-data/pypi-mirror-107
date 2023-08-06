"""
Type annotations for storagegateway service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_storagegateway import StorageGatewayClient
    from mypy_boto3_storagegateway.paginator import (
        DescribeTapeArchivesPaginator,
        DescribeTapeRecoveryPointsPaginator,
        DescribeTapesPaginator,
        DescribeVTLDevicesPaginator,
        ListFileSharesPaginator,
        ListFileSystemAssociationsPaginator,
        ListGatewaysPaginator,
        ListTagsForResourcePaginator,
        ListTapePoolsPaginator,
        ListTapesPaginator,
        ListVolumesPaginator,
    )

    client: StorageGatewayClient = boto3.client("storagegateway")

    describe_tape_archives_paginator: DescribeTapeArchivesPaginator = client.get_paginator("describe_tape_archives")
    describe_tape_recovery_points_paginator: DescribeTapeRecoveryPointsPaginator = client.get_paginator("describe_tape_recovery_points")
    describe_tapes_paginator: DescribeTapesPaginator = client.get_paginator("describe_tapes")
    describe_vtl_devices_paginator: DescribeVTLDevicesPaginator = client.get_paginator("describe_vtl_devices")
    list_file_shares_paginator: ListFileSharesPaginator = client.get_paginator("list_file_shares")
    list_file_system_associations_paginator: ListFileSystemAssociationsPaginator = client.get_paginator("list_file_system_associations")
    list_gateways_paginator: ListGatewaysPaginator = client.get_paginator("list_gateways")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_tape_pools_paginator: ListTapePoolsPaginator = client.get_paginator("list_tape_pools")
    list_tapes_paginator: ListTapesPaginator = client.get_paginator("list_tapes")
    list_volumes_paginator: ListVolumesPaginator = client.get_paginator("list_volumes")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeTapeArchivesOutputTypeDef,
    DescribeTapeRecoveryPointsOutputTypeDef,
    DescribeTapesOutputTypeDef,
    DescribeVTLDevicesOutputTypeDef,
    ListFileSharesOutputTypeDef,
    ListFileSystemAssociationsOutputTypeDef,
    ListGatewaysOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTapePoolsOutputTypeDef,
    ListTapesOutputTypeDef,
    ListVolumesOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeTapeArchivesPaginator",
    "DescribeTapeRecoveryPointsPaginator",
    "DescribeTapesPaginator",
    "DescribeVTLDevicesPaginator",
    "ListFileSharesPaginator",
    "ListFileSystemAssociationsPaginator",
    "ListGatewaysPaginator",
    "ListTagsForResourcePaginator",
    "ListTapePoolsPaginator",
    "ListTapesPaginator",
    "ListVolumesPaginator",
)


class DescribeTapeArchivesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapeArchives)[Show boto3-stubs documentation](./paginators.md#describetapearchivespaginator)
    """

    def paginate(
        self, TapeARNs: List[str] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeTapeArchivesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapeArchives.paginate)
        [Show boto3-stubs documentation](./paginators.md#describetapearchivespaginator)
        """


class DescribeTapeRecoveryPointsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapeRecoveryPoints)[Show boto3-stubs documentation](./paginators.md#describetaperecoverypointspaginator)
    """

    def paginate(
        self, GatewayARN: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeTapeRecoveryPointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapeRecoveryPoints.paginate)
        [Show boto3-stubs documentation](./paginators.md#describetaperecoverypointspaginator)
        """


class DescribeTapesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapes)[Show boto3-stubs documentation](./paginators.md#describetapespaginator)
    """

    def paginate(
        self,
        GatewayARN: str,
        TapeARNs: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeTapesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapes.paginate)
        [Show boto3-stubs documentation](./paginators.md#describetapespaginator)
        """


class DescribeVTLDevicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeVTLDevices)[Show boto3-stubs documentation](./paginators.md#describevtldevicespaginator)
    """

    def paginate(
        self,
        GatewayARN: str,
        VTLDeviceARNs: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeVTLDevicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeVTLDevices.paginate)
        [Show boto3-stubs documentation](./paginators.md#describevtldevicespaginator)
        """


class ListFileSharesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListFileShares)[Show boto3-stubs documentation](./paginators.md#listfilesharespaginator)
    """

    def paginate(
        self, GatewayARN: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListFileSharesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListFileShares.paginate)
        [Show boto3-stubs documentation](./paginators.md#listfilesharespaginator)
        """


class ListFileSystemAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListFileSystemAssociations)[Show boto3-stubs documentation](./paginators.md#listfilesystemassociationspaginator)
    """

    def paginate(
        self, GatewayARN: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListFileSystemAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListFileSystemAssociations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listfilesystemassociationspaginator)
        """


class ListGatewaysPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListGateways)[Show boto3-stubs documentation](./paginators.md#listgatewayspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListGatewaysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListGateways.paginate)
        [Show boto3-stubs documentation](./paginators.md#listgatewayspaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListTagsForResource)[Show boto3-stubs documentation](./paginators.md#listtagsforresourcepaginator)
    """

    def paginate(
        self, ResourceARN: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtagsforresourcepaginator)
        """


class ListTapePoolsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListTapePools)[Show boto3-stubs documentation](./paginators.md#listtapepoolspaginator)
    """

    def paginate(
        self, PoolARNs: List[str] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTapePoolsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListTapePools.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtapepoolspaginator)
        """


class ListTapesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListTapes)[Show boto3-stubs documentation](./paginators.md#listtapespaginator)
    """

    def paginate(
        self, TapeARNs: List[str] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTapesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListTapes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtapespaginator)
        """


class ListVolumesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListVolumes)[Show boto3-stubs documentation](./paginators.md#listvolumespaginator)
    """

    def paginate(
        self, GatewayARN: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListVolumesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/storagegateway.html#StorageGateway.Paginator.ListVolumes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listvolumespaginator)
        """
