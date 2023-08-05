"""
Type annotations for s3 service client waiters.

[Open documentation](./waiters.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.waiter import (
        BucketExistsWaiter,
        BucketNotExistsWaiter,
        ObjectExistsWaiter,
        ObjectNotExistsWaiter,
    )

    client: S3Client = boto3.client("s3")

    bucket_exists_waiter: BucketExistsWaiter = client.get_waiter("bucket_exists")
    bucket_not_exists_waiter: BucketNotExistsWaiter = client.get_waiter("bucket_not_exists")
    object_exists_waiter: ObjectExistsWaiter = client.get_waiter("object_exists")
    object_not_exists_waiter: ObjectNotExistsWaiter = client.get_waiter("object_not_exists")
    ```
"""
import sys
from datetime import datetime

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "BucketExistsWaiter",
    "BucketNotExistsWaiter",
    "ObjectExistsWaiter",
    "ObjectNotExistsWaiter",
)


class BucketExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/s3.html#S3.Waiter.bucket_exists)[Show boto3-stubs documentation](./waiters.md#bucketexistswaiter)
    """

    def wait(
        self, Bucket: str, ExpectedBucketOwner: str = None, WaiterConfig: WaiterConfigTypeDef = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/s3.html#S3.Waiter.BucketExistsWaiter)
        [Show boto3-stubs documentation](./waiters.md#bucketexists)
        """


class BucketNotExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/s3.html#S3.Waiter.bucket_not_exists)[Show boto3-stubs documentation](./waiters.md#bucketnotexistswaiter)
    """

    def wait(
        self, Bucket: str, ExpectedBucketOwner: str = None, WaiterConfig: WaiterConfigTypeDef = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/s3.html#S3.Waiter.BucketNotExistsWaiter)
        [Show boto3-stubs documentation](./waiters.md#bucketnotexists)
        """


class ObjectExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/s3.html#S3.Waiter.object_exists)[Show boto3-stubs documentation](./waiters.md#objectexistswaiter)
    """

    def wait(
        self,
        Bucket: str,
        Key: str,
        IfMatch: str = None,
        IfModifiedSince: datetime = None,
        IfNoneMatch: str = None,
        IfUnmodifiedSince: datetime = None,
        Range: str = None,
        VersionId: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        PartNumber: int = None,
        ExpectedBucketOwner: str = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/s3.html#S3.Waiter.ObjectExistsWaiter)
        [Show boto3-stubs documentation](./waiters.md#objectexists)
        """


class ObjectNotExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/s3.html#S3.Waiter.object_not_exists)[Show boto3-stubs documentation](./waiters.md#objectnotexistswaiter)
    """

    def wait(
        self,
        Bucket: str,
        Key: str,
        IfMatch: str = None,
        IfModifiedSince: datetime = None,
        IfNoneMatch: str = None,
        IfUnmodifiedSince: datetime = None,
        Range: str = None,
        VersionId: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        PartNumber: int = None,
        ExpectedBucketOwner: str = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/s3.html#S3.Waiter.ObjectNotExistsWaiter)
        [Show boto3-stubs documentation](./waiters.md#objectnotexists)
        """
