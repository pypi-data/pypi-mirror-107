"""
Type annotations for cloudfront service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_cloudfront import CloudFrontClient
    from mypy_boto3_cloudfront.paginator import (
        ListCloudFrontOriginAccessIdentitiesPaginator,
        ListDistributionsPaginator,
        ListInvalidationsPaginator,
        ListStreamingDistributionsPaginator,
    )

    client: CloudFrontClient = boto3.client("cloudfront")

    list_cloud_front_origin_access_identities_paginator: ListCloudFrontOriginAccessIdentitiesPaginator = client.get_paginator("list_cloud_front_origin_access_identities")
    list_distributions_paginator: ListDistributionsPaginator = client.get_paginator("list_distributions")
    list_invalidations_paginator: ListInvalidationsPaginator = client.get_paginator("list_invalidations")
    list_streaming_distributions_paginator: ListStreamingDistributionsPaginator = client.get_paginator("list_streaming_distributions")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListCloudFrontOriginAccessIdentitiesResultTypeDef,
    ListDistributionsResultTypeDef,
    ListInvalidationsResultTypeDef,
    ListStreamingDistributionsResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListCloudFrontOriginAccessIdentitiesPaginator",
    "ListDistributionsPaginator",
    "ListInvalidationsPaginator",
    "ListStreamingDistributionsPaginator",
)


class ListCloudFrontOriginAccessIdentitiesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudfront.html#CloudFront.Paginator.ListCloudFrontOriginAccessIdentities)[Show boto3-stubs documentation](./paginators.md#listcloudfrontoriginaccessidentitiespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListCloudFrontOriginAccessIdentitiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudfront.html#CloudFront.Paginator.ListCloudFrontOriginAccessIdentities.paginate)
        [Show boto3-stubs documentation](./paginators.md#listcloudfrontoriginaccessidentitiespaginator)
        """


class ListDistributionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudfront.html#CloudFront.Paginator.ListDistributions)[Show boto3-stubs documentation](./paginators.md#listdistributionspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListDistributionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudfront.html#CloudFront.Paginator.ListDistributions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdistributionspaginator)
        """


class ListInvalidationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudfront.html#CloudFront.Paginator.ListInvalidations)[Show boto3-stubs documentation](./paginators.md#listinvalidationspaginator)
    """

    def paginate(
        self, DistributionId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListInvalidationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudfront.html#CloudFront.Paginator.ListInvalidations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listinvalidationspaginator)
        """


class ListStreamingDistributionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudfront.html#CloudFront.Paginator.ListStreamingDistributions)[Show boto3-stubs documentation](./paginators.md#liststreamingdistributionspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListStreamingDistributionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudfront.html#CloudFront.Paginator.ListStreamingDistributions.paginate)
        [Show boto3-stubs documentation](./paginators.md#liststreamingdistributionspaginator)
        """
