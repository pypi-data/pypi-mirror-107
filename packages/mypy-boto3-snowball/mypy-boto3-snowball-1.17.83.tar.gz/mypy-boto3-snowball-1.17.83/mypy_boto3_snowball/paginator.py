"""
Type annotations for snowball service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_snowball import SnowballClient
    from mypy_boto3_snowball.paginator import (
        DescribeAddressesPaginator,
        ListClusterJobsPaginator,
        ListClustersPaginator,
        ListCompatibleImagesPaginator,
        ListJobsPaginator,
    )

    client: SnowballClient = boto3.client("snowball")

    describe_addresses_paginator: DescribeAddressesPaginator = client.get_paginator("describe_addresses")
    list_cluster_jobs_paginator: ListClusterJobsPaginator = client.get_paginator("list_cluster_jobs")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_compatible_images_paginator: ListCompatibleImagesPaginator = client.get_paginator("list_compatible_images")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeAddressesResultTypeDef,
    ListClusterJobsResultTypeDef,
    ListClustersResultTypeDef,
    ListCompatibleImagesResultTypeDef,
    ListJobsResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeAddressesPaginator",
    "ListClusterJobsPaginator",
    "ListClustersPaginator",
    "ListCompatibleImagesPaginator",
    "ListJobsPaginator",
)


class DescribeAddressesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/snowball.html#Snowball.Paginator.DescribeAddresses)[Show boto3-stubs documentation](./paginators.md#describeaddressespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeAddressesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/snowball.html#Snowball.Paginator.DescribeAddresses.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeaddressespaginator)
        """


class ListClusterJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/snowball.html#Snowball.Paginator.ListClusterJobs)[Show boto3-stubs documentation](./paginators.md#listclusterjobspaginator)
    """

    def paginate(
        self, ClusterId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListClusterJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/snowball.html#Snowball.Paginator.ListClusterJobs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listclusterjobspaginator)
        """


class ListClustersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/snowball.html#Snowball.Paginator.ListClusters)[Show boto3-stubs documentation](./paginators.md#listclusterspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListClustersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/snowball.html#Snowball.Paginator.ListClusters.paginate)
        [Show boto3-stubs documentation](./paginators.md#listclusterspaginator)
        """


class ListCompatibleImagesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/snowball.html#Snowball.Paginator.ListCompatibleImages)[Show boto3-stubs documentation](./paginators.md#listcompatibleimagespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListCompatibleImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/snowball.html#Snowball.Paginator.ListCompatibleImages.paginate)
        [Show boto3-stubs documentation](./paginators.md#listcompatibleimagespaginator)
        """


class ListJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/snowball.html#Snowball.Paginator.ListJobs)[Show boto3-stubs documentation](./paginators.md#listjobspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/snowball.html#Snowball.Paginator.ListJobs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listjobspaginator)
        """
