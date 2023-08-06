"""
Type annotations for route53 service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_route53 import Route53Client
    from mypy_boto3_route53.paginator import (
        ListHealthChecksPaginator,
        ListHostedZonesPaginator,
        ListQueryLoggingConfigsPaginator,
        ListResourceRecordSetsPaginator,
        ListVPCAssociationAuthorizationsPaginator,
    )

    client: Route53Client = boto3.client("route53")

    list_health_checks_paginator: ListHealthChecksPaginator = client.get_paginator("list_health_checks")
    list_hosted_zones_paginator: ListHostedZonesPaginator = client.get_paginator("list_hosted_zones")
    list_query_logging_configs_paginator: ListQueryLoggingConfigsPaginator = client.get_paginator("list_query_logging_configs")
    list_resource_record_sets_paginator: ListResourceRecordSetsPaginator = client.get_paginator("list_resource_record_sets")
    list_vpc_association_authorizations_paginator: ListVPCAssociationAuthorizationsPaginator = client.get_paginator("list_vpc_association_authorizations")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListHealthChecksResponseTypeDef,
    ListHostedZonesResponseTypeDef,
    ListQueryLoggingConfigsResponseTypeDef,
    ListResourceRecordSetsResponseTypeDef,
    ListVPCAssociationAuthorizationsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListHealthChecksPaginator",
    "ListHostedZonesPaginator",
    "ListQueryLoggingConfigsPaginator",
    "ListResourceRecordSetsPaginator",
    "ListVPCAssociationAuthorizationsPaginator",
)


class ListHealthChecksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/route53.html#Route53.Paginator.ListHealthChecks)[Show boto3-stubs documentation](./paginators.md#listhealthcheckspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListHealthChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/route53.html#Route53.Paginator.ListHealthChecks.paginate)
        [Show boto3-stubs documentation](./paginators.md#listhealthcheckspaginator)
        """


class ListHostedZonesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/route53.html#Route53.Paginator.ListHostedZones)[Show boto3-stubs documentation](./paginators.md#listhostedzonespaginator)
    """

    def paginate(
        self, DelegationSetId: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListHostedZonesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/route53.html#Route53.Paginator.ListHostedZones.paginate)
        [Show boto3-stubs documentation](./paginators.md#listhostedzonespaginator)
        """


class ListQueryLoggingConfigsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/route53.html#Route53.Paginator.ListQueryLoggingConfigs)[Show boto3-stubs documentation](./paginators.md#listqueryloggingconfigspaginator)
    """

    def paginate(
        self, HostedZoneId: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListQueryLoggingConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/route53.html#Route53.Paginator.ListQueryLoggingConfigs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listqueryloggingconfigspaginator)
        """


class ListResourceRecordSetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/route53.html#Route53.Paginator.ListResourceRecordSets)[Show boto3-stubs documentation](./paginators.md#listresourcerecordsetspaginator)
    """

    def paginate(
        self, HostedZoneId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListResourceRecordSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/route53.html#Route53.Paginator.ListResourceRecordSets.paginate)
        [Show boto3-stubs documentation](./paginators.md#listresourcerecordsetspaginator)
        """


class ListVPCAssociationAuthorizationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/route53.html#Route53.Paginator.ListVPCAssociationAuthorizations)[Show boto3-stubs documentation](./paginators.md#listvpcassociationauthorizationspaginator)
    """

    def paginate(
        self,
        HostedZoneId: str,
        MaxResults: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListVPCAssociationAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/route53.html#Route53.Paginator.ListVPCAssociationAuthorizations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listvpcassociationauthorizationspaginator)
        """
