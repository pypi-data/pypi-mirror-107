"""
Type annotations for mediastore-data service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_mediastore_data import MediaStoreDataClient
    from mypy_boto3_mediastore_data.paginator import (
        ListItemsPaginator,
    )

    client: MediaStoreDataClient = boto3.client("mediastore-data")

    list_items_paginator: ListItemsPaginator = client.get_paginator("list_items")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import ListItemsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListItemsPaginator",)

class ListItemsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediastore-data.html#MediaStoreData.Paginator.ListItems)[Show boto3-stubs documentation](./paginators.md#listitemspaginator)
    """

    def paginate(
        self, Path: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediastore-data.html#MediaStoreData.Paginator.ListItems.paginate)
        [Show boto3-stubs documentation](./paginators.md#listitemspaginator)
        """
