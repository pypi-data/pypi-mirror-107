"""
Type annotations for s3outposts service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_s3outposts import S3OutpostsClient
    from mypy_boto3_s3outposts.paginator import (
        ListEndpointsPaginator,
    )

    client: S3OutpostsClient = boto3.client("s3outposts")

    list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import ListEndpointsResultTypeDef, PaginatorConfigTypeDef

__all__ = ("ListEndpointsPaginator",)


class ListEndpointsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/s3outposts.html#S3Outposts.Paginator.ListEndpoints)[Show boto3-stubs documentation](./paginators.md#listendpointspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/s3outposts.html#S3Outposts.Paginator.ListEndpoints.paginate)
        [Show boto3-stubs documentation](./paginators.md#listendpointspaginator)
        """
