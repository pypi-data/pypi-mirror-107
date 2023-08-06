"""
Type annotations for s3outposts service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_s3outposts.literals import EndpointStatusType

    data: EndpointStatusType = "AVAILABLE"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("EndpointStatusType", "ListEndpointsPaginatorName")

EndpointStatusType = Literal["AVAILABLE", "PENDING"]
ListEndpointsPaginatorName = Literal["list_endpoints"]
