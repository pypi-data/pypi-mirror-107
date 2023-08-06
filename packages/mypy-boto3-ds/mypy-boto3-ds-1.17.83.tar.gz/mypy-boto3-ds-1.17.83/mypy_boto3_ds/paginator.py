"""
Type annotations for ds service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_ds import DirectoryServiceClient
    from mypy_boto3_ds.paginator import (
        DescribeDirectoriesPaginator,
        DescribeDomainControllersPaginator,
        DescribeSharedDirectoriesPaginator,
        DescribeSnapshotsPaginator,
        DescribeTrustsPaginator,
        ListIpRoutesPaginator,
        ListLogSubscriptionsPaginator,
        ListSchemaExtensionsPaginator,
        ListTagsForResourcePaginator,
    )

    client: DirectoryServiceClient = boto3.client("ds")

    describe_directories_paginator: DescribeDirectoriesPaginator = client.get_paginator("describe_directories")
    describe_domain_controllers_paginator: DescribeDomainControllersPaginator = client.get_paginator("describe_domain_controllers")
    describe_shared_directories_paginator: DescribeSharedDirectoriesPaginator = client.get_paginator("describe_shared_directories")
    describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
    describe_trusts_paginator: DescribeTrustsPaginator = client.get_paginator("describe_trusts")
    list_ip_routes_paginator: ListIpRoutesPaginator = client.get_paginator("list_ip_routes")
    list_log_subscriptions_paginator: ListLogSubscriptionsPaginator = client.get_paginator("list_log_subscriptions")
    list_schema_extensions_paginator: ListSchemaExtensionsPaginator = client.get_paginator("list_schema_extensions")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeDirectoriesResultTypeDef,
    DescribeDomainControllersResultTypeDef,
    DescribeSharedDirectoriesResultTypeDef,
    DescribeSnapshotsResultTypeDef,
    DescribeTrustsResultTypeDef,
    ListIpRoutesResultTypeDef,
    ListLogSubscriptionsResultTypeDef,
    ListSchemaExtensionsResultTypeDef,
    ListTagsForResourceResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeDirectoriesPaginator",
    "DescribeDomainControllersPaginator",
    "DescribeSharedDirectoriesPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeTrustsPaginator",
    "ListIpRoutesPaginator",
    "ListLogSubscriptionsPaginator",
    "ListSchemaExtensionsPaginator",
    "ListTagsForResourcePaginator",
)


class DescribeDirectoriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.DescribeDirectories)[Show boto3-stubs documentation](./paginators.md#describedirectoriespaginator)
    """

    def paginate(
        self, DirectoryIds: List[str] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeDirectoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.DescribeDirectories.paginate)
        [Show boto3-stubs documentation](./paginators.md#describedirectoriespaginator)
        """


class DescribeDomainControllersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.DescribeDomainControllers)[Show boto3-stubs documentation](./paginators.md#describedomaincontrollerspaginator)
    """

    def paginate(
        self,
        DirectoryId: str,
        DomainControllerIds: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeDomainControllersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.DescribeDomainControllers.paginate)
        [Show boto3-stubs documentation](./paginators.md#describedomaincontrollerspaginator)
        """


class DescribeSharedDirectoriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.DescribeSharedDirectories)[Show boto3-stubs documentation](./paginators.md#describeshareddirectoriespaginator)
    """

    def paginate(
        self,
        OwnerDirectoryId: str,
        SharedDirectoryIds: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeSharedDirectoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.DescribeSharedDirectories.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeshareddirectoriespaginator)
        """


class DescribeSnapshotsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.DescribeSnapshots)[Show boto3-stubs documentation](./paginators.md#describesnapshotspaginator)
    """

    def paginate(
        self,
        DirectoryId: str = None,
        SnapshotIds: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.DescribeSnapshots.paginate)
        [Show boto3-stubs documentation](./paginators.md#describesnapshotspaginator)
        """


class DescribeTrustsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.DescribeTrusts)[Show boto3-stubs documentation](./paginators.md#describetrustspaginator)
    """

    def paginate(
        self,
        DirectoryId: str = None,
        TrustIds: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeTrustsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.DescribeTrusts.paginate)
        [Show boto3-stubs documentation](./paginators.md#describetrustspaginator)
        """


class ListIpRoutesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.ListIpRoutes)[Show boto3-stubs documentation](./paginators.md#listiproutespaginator)
    """

    def paginate(
        self, DirectoryId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListIpRoutesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.ListIpRoutes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listiproutespaginator)
        """


class ListLogSubscriptionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.ListLogSubscriptions)[Show boto3-stubs documentation](./paginators.md#listlogsubscriptionspaginator)
    """

    def paginate(
        self, DirectoryId: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListLogSubscriptionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.ListLogSubscriptions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listlogsubscriptionspaginator)
        """


class ListSchemaExtensionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.ListSchemaExtensions)[Show boto3-stubs documentation](./paginators.md#listschemaextensionspaginator)
    """

    def paginate(
        self, DirectoryId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSchemaExtensionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.ListSchemaExtensions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listschemaextensionspaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.ListTagsForResource)[Show boto3-stubs documentation](./paginators.md#listtagsforresourcepaginator)
    """

    def paginate(
        self, ResourceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTagsForResourceResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/ds.html#DirectoryService.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](./paginators.md#listtagsforresourcepaginator)
        """
