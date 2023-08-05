"""
Type annotations for mediastore-data service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_mediastore_data import MediaStoreDataClient

    client: MediaStoreDataClient = boto3.client("mediastore-data")
    ```
"""
import sys
from typing import IO, Any, Dict, Type, Union

from botocore.client import ClientMeta

from .literals import UploadAvailabilityType
from .paginator import ListItemsPaginator
from .type_defs import (
    DescribeObjectResponseTypeDef,
    GetObjectResponseTypeDef,
    ListItemsResponseTypeDef,
    PutObjectResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("MediaStoreDataClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str
    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ContainerNotFoundException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    ObjectNotFoundException: Type[BotocoreClientError]
    RequestedRangeNotSatisfiableException: Type[BotocoreClientError]

class MediaStoreDataClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediastore-data.html#MediaStoreData.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions
    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediastore-data.html#MediaStoreData.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can_paginate)
        """
    def delete_object(self, Path: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediastore-data.html#MediaStoreData.Client.delete_object)
        [Show boto3-stubs documentation](./client.md#delete_object)
        """
    def describe_object(self, Path: str) -> DescribeObjectResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediastore-data.html#MediaStoreData.Client.describe_object)
        [Show boto3-stubs documentation](./client.md#describe_object)
        """
    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediastore-data.html#MediaStoreData.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate_presigned_url)
        """
    def get_object(self, Path: str, Range: str = None) -> GetObjectResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediastore-data.html#MediaStoreData.Client.get_object)
        [Show boto3-stubs documentation](./client.md#get_object)
        """
    def list_items(
        self, Path: str = None, MaxResults: int = None, NextToken: str = None
    ) -> ListItemsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediastore-data.html#MediaStoreData.Client.list_items)
        [Show boto3-stubs documentation](./client.md#list_items)
        """
    def put_object(
        self,
        Body: Union[bytes, IO[bytes]],
        Path: str,
        ContentType: str = None,
        CacheControl: str = None,
        StorageClass: Literal["TEMPORAL"] = None,
        UploadAvailability: UploadAvailabilityType = None,
    ) -> PutObjectResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediastore-data.html#MediaStoreData.Client.put_object)
        [Show boto3-stubs documentation](./client.md#put_object)
        """
    def get_paginator(self, operation_name: Literal["list_items"]) -> ListItemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediastore-data.html#MediaStoreData.Paginator.ListItems)[Show boto3-stubs documentation](./paginators.md#listitemspaginator)
        """
