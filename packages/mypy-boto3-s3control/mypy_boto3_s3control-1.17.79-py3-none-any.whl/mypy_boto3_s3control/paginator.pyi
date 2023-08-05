"""
Type annotations for s3control service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_s3control import S3ControlClient
    from mypy_boto3_s3control.paginator import (
        ListAccessPointsForObjectLambdaPaginator,
    )

    client: S3ControlClient = boto3.client("s3control")

    list_access_points_for_object_lambda_paginator: ListAccessPointsForObjectLambdaPaginator = client.get_paginator("list_access_points_for_object_lambda")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import ListAccessPointsForObjectLambdaResultTypeDef, PaginatorConfigTypeDef

__all__ = ("ListAccessPointsForObjectLambdaPaginator",)

class ListAccessPointsForObjectLambdaPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/s3control.html#S3Control.Paginator.ListAccessPointsForObjectLambda)[Show boto3-stubs documentation](./paginators.md#listaccesspointsforobjectlambdapaginator)
    """

    def paginate(
        self, AccountId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListAccessPointsForObjectLambdaResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/s3control.html#S3Control.Paginator.ListAccessPointsForObjectLambda.paginate)
        [Show boto3-stubs documentation](./paginators.md#listaccesspointsforobjectlambdapaginator)
        """
