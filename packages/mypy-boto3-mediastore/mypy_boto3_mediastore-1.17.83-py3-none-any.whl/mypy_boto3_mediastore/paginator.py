"""
Type annotations for mediastore service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_mediastore import MediaStoreClient
    from mypy_boto3_mediastore.paginator import (
        ListContainersPaginator,
    )

    client: MediaStoreClient = boto3.client("mediastore")

    list_containers_paginator: ListContainersPaginator = client.get_paginator("list_containers")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import ListContainersOutputTypeDef, PaginatorConfigTypeDef

__all__ = ("ListContainersPaginator",)


class ListContainersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/mediastore.html#MediaStore.Paginator.ListContainers)[Show boto3-stubs documentation](./paginators.md#listcontainerspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListContainersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/mediastore.html#MediaStore.Paginator.ListContainers.paginate)
        [Show boto3-stubs documentation](./paginators.md#listcontainerspaginator)
        """
