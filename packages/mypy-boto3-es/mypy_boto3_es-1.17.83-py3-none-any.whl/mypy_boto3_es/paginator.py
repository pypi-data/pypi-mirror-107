"""
Type annotations for es service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_es import ElasticsearchServiceClient
    from mypy_boto3_es.paginator import (
        DescribeReservedElasticsearchInstanceOfferingsPaginator,
        DescribeReservedElasticsearchInstancesPaginator,
        GetUpgradeHistoryPaginator,
        ListElasticsearchInstanceTypesPaginator,
        ListElasticsearchVersionsPaginator,
    )

    client: ElasticsearchServiceClient = boto3.client("es")

    describe_reserved_elasticsearch_instance_offerings_paginator: DescribeReservedElasticsearchInstanceOfferingsPaginator = client.get_paginator("describe_reserved_elasticsearch_instance_offerings")
    describe_reserved_elasticsearch_instances_paginator: DescribeReservedElasticsearchInstancesPaginator = client.get_paginator("describe_reserved_elasticsearch_instances")
    get_upgrade_history_paginator: GetUpgradeHistoryPaginator = client.get_paginator("get_upgrade_history")
    list_elasticsearch_instance_types_paginator: ListElasticsearchInstanceTypesPaginator = client.get_paginator("list_elasticsearch_instance_types")
    list_elasticsearch_versions_paginator: ListElasticsearchVersionsPaginator = client.get_paginator("list_elasticsearch_versions")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef,
    DescribeReservedElasticsearchInstancesResponseTypeDef,
    GetUpgradeHistoryResponseTypeDef,
    ListElasticsearchInstanceTypesResponseTypeDef,
    ListElasticsearchVersionsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeReservedElasticsearchInstanceOfferingsPaginator",
    "DescribeReservedElasticsearchInstancesPaginator",
    "GetUpgradeHistoryPaginator",
    "ListElasticsearchInstanceTypesPaginator",
    "ListElasticsearchVersionsPaginator",
)


class DescribeReservedElasticsearchInstanceOfferingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/es.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstanceOfferings)[Show boto3-stubs documentation](./paginators.md#describereservedelasticsearchinstanceofferingspaginator)
    """

    def paginate(
        self,
        ReservedElasticsearchInstanceOfferingId: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/es.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstanceOfferings.paginate)
        [Show boto3-stubs documentation](./paginators.md#describereservedelasticsearchinstanceofferingspaginator)
        """


class DescribeReservedElasticsearchInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/es.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstances)[Show boto3-stubs documentation](./paginators.md#describereservedelasticsearchinstancespaginator)
    """

    def paginate(
        self,
        ReservedElasticsearchInstanceId: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeReservedElasticsearchInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/es.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstances.paginate)
        [Show boto3-stubs documentation](./paginators.md#describereservedelasticsearchinstancespaginator)
        """


class GetUpgradeHistoryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/es.html#ElasticsearchService.Paginator.GetUpgradeHistory)[Show boto3-stubs documentation](./paginators.md#getupgradehistorypaginator)
    """

    def paginate(
        self, DomainName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[GetUpgradeHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/es.html#ElasticsearchService.Paginator.GetUpgradeHistory.paginate)
        [Show boto3-stubs documentation](./paginators.md#getupgradehistorypaginator)
        """


class ListElasticsearchInstanceTypesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/es.html#ElasticsearchService.Paginator.ListElasticsearchInstanceTypes)[Show boto3-stubs documentation](./paginators.md#listelasticsearchinstancetypespaginator)
    """

    def paginate(
        self,
        ElasticsearchVersion: str,
        DomainName: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListElasticsearchInstanceTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/es.html#ElasticsearchService.Paginator.ListElasticsearchInstanceTypes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listelasticsearchinstancetypespaginator)
        """


class ListElasticsearchVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/es.html#ElasticsearchService.Paginator.ListElasticsearchVersions)[Show boto3-stubs documentation](./paginators.md#listelasticsearchversionspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListElasticsearchVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/es.html#ElasticsearchService.Paginator.ListElasticsearchVersions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listelasticsearchversionspaginator)
        """
