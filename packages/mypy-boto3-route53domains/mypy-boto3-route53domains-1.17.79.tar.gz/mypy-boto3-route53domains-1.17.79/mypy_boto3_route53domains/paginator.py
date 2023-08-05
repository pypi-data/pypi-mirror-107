"""
Type annotations for route53domains service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_route53domains import Route53DomainsClient
    from mypy_boto3_route53domains.paginator import (
        ListDomainsPaginator,
        ListOperationsPaginator,
        ViewBillingPaginator,
    )

    client: Route53DomainsClient = boto3.client("route53domains")

    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
    view_billing_paginator: ViewBillingPaginator = client.get_paginator("view_billing")
    ```
"""
from datetime import datetime
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListDomainsResponseTypeDef,
    ListOperationsResponseTypeDef,
    PaginatorConfigTypeDef,
    ViewBillingResponseTypeDef,
)

__all__ = ("ListDomainsPaginator", "ListOperationsPaginator", "ViewBillingPaginator")


class ListDomainsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/route53domains.html#Route53Domains.Paginator.ListDomains)[Show boto3-stubs documentation](./paginators.md#listdomainspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/route53domains.html#Route53Domains.Paginator.ListDomains.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdomainspaginator)
        """


class ListOperationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/route53domains.html#Route53Domains.Paginator.ListOperations)[Show boto3-stubs documentation](./paginators.md#listoperationspaginator)
    """

    def paginate(
        self, SubmittedSince: datetime = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/route53domains.html#Route53Domains.Paginator.ListOperations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listoperationspaginator)
        """


class ViewBillingPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/route53domains.html#Route53Domains.Paginator.ViewBilling)[Show boto3-stubs documentation](./paginators.md#viewbillingpaginator)
    """

    def paginate(
        self,
        Start: datetime = None,
        End: datetime = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ViewBillingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/route53domains.html#Route53Domains.Paginator.ViewBilling.paginate)
        [Show boto3-stubs documentation](./paginators.md#viewbillingpaginator)
        """
