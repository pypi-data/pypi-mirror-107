"""
Type annotations for s3 service ServiceResource

[Open documentation](./service_resource.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_s3 import S3ServiceResource
    import mypy_boto3_s3.service_resource as s3_resources

    resource: S3ServiceResource = boto3.resource("s3")

    my_bucket: s3_resources.Bucket = resource.Bucket(...)
    my_bucket_acl: s3_resources.BucketAcl = resource.BucketAcl(...)
    my_bucket_cors: s3_resources.BucketCors = resource.BucketCors(...)
    my_bucket_lifecycle: s3_resources.BucketLifecycle = resource.BucketLifecycle(...)
    my_bucket_lifecycle_configuration: s3_resources.BucketLifecycleConfiguration = resource.BucketLifecycleConfiguration(...)
    my_bucket_logging: s3_resources.BucketLogging = resource.BucketLogging(...)
    my_bucket_notification: s3_resources.BucketNotification = resource.BucketNotification(...)
    my_bucket_policy: s3_resources.BucketPolicy = resource.BucketPolicy(...)
    my_bucket_request_payment: s3_resources.BucketRequestPayment = resource.BucketRequestPayment(...)
    my_bucket_tagging: s3_resources.BucketTagging = resource.BucketTagging(...)
    my_bucket_versioning: s3_resources.BucketVersioning = resource.BucketVersioning(...)
    my_bucket_website: s3_resources.BucketWebsite = resource.BucketWebsite(...)
    my_multipart_upload: s3_resources.MultipartUpload = resource.MultipartUpload(...)
    my_multipart_upload_part: s3_resources.MultipartUploadPart = resource.MultipartUploadPart(...)
    my_object: s3_resources.Object = resource.Object(...)
    my_object_acl: s3_resources.ObjectAcl = resource.ObjectAcl(...)
    my_object_summary: s3_resources.ObjectSummary = resource.ObjectSummary(...)
    my_object_version: s3_resources.ObjectVersion = resource.ObjectVersion(...)
```
"""
import sys
from datetime import datetime
from typing import IO, Any, Callable, Dict, Iterator, List, Union

from boto3.resources.base import ServiceResource as Boto3ServiceResource
from boto3.resources.collection import ResourceCollection
from boto3.s3.transfer import TransferConfig
from botocore.client import BaseClient

from .literals import (
    BucketCannedACLType,
    MetadataDirectiveType,
    ObjectCannedACLType,
    ObjectLockLegalHoldStatusType,
    ObjectLockModeType,
    ServerSideEncryptionType,
    StorageClassType,
    TaggingDirectiveType,
)
from .type_defs import (
    AbortMultipartUploadOutputTypeDef,
    AccessControlPolicyTypeDef,
    BucketLifecycleConfigurationTypeDef,
    BucketLoggingStatusTypeDef,
    CompletedMultipartUploadTypeDef,
    CopyObjectOutputTypeDef,
    CopySourceTypeDef,
    CORSConfigurationTypeDef,
    CreateBucketConfigurationTypeDef,
    CreateBucketOutputTypeDef,
    DeleteObjectOutputTypeDef,
    DeleteObjectsOutputTypeDef,
    DeleteTypeDef,
    GetObjectOutputTypeDef,
    HeadObjectOutputTypeDef,
    LifecycleConfigurationTypeDef,
    NotificationConfigurationTypeDef,
    PutObjectAclOutputTypeDef,
    PutObjectOutputTypeDef,
    RequestPaymentConfigurationTypeDef,
    RestoreObjectOutputTypeDef,
    RestoreRequestTypeDef,
    TaggingTypeDef,
    UploadPartCopyOutputTypeDef,
    UploadPartOutputTypeDef,
    VersioningConfigurationTypeDef,
    WebsiteConfigurationTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "S3ServiceResource",
    "Bucket",
    "BucketAcl",
    "BucketCors",
    "BucketLifecycle",
    "BucketLifecycleConfiguration",
    "BucketLogging",
    "BucketNotification",
    "BucketPolicy",
    "BucketRequestPayment",
    "BucketTagging",
    "BucketVersioning",
    "BucketWebsite",
    "MultipartUpload",
    "MultipartUploadPart",
    "Object",
    "ObjectAcl",
    "ObjectSummary",
    "ObjectVersion",
    "ServiceResourceBucketsCollection",
    "BucketMultipartUploadsCollection",
    "BucketObjectVersionsCollection",
    "BucketObjectsCollection",
    "MultipartUploadPartsCollection",
)


class ServiceResourceBucketsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.buckets)
    [Show boto3-stubs documentation](./service_resource.md#serviceresourcebucketscollection)
    """

    def all(self) -> "ServiceResourceBucketsCollection":
        pass

    def filter(self) -> "ServiceResourceBucketsCollection":  # type: ignore
        pass

    def limit(self, count: int) -> "ServiceResourceBucketsCollection":
        pass

    def page_size(self, count: int) -> "ServiceResourceBucketsCollection":
        pass

    def pages(self) -> Iterator[List["Bucket"]]:
        pass

    def __iter__(self) -> Iterator["Bucket"]:
        pass


class BucketMultipartUploadsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.multipart_uploads)
    [Show boto3-stubs documentation](./service_resource.md#bucketmultipartuploadscollection)
    """

    def all(self) -> "BucketMultipartUploadsCollection":
        pass

    def filter(  # type: ignore
        self,
        Delimiter: str = None,
        EncodingType: Literal["url"] = None,
        KeyMarker: str = None,
        MaxUploads: int = None,
        Prefix: str = None,
        UploadIdMarker: str = None,
        ExpectedBucketOwner: str = None,
    ) -> "BucketMultipartUploadsCollection":
        pass

    def limit(self, count: int) -> "BucketMultipartUploadsCollection":
        pass

    def page_size(self, count: int) -> "BucketMultipartUploadsCollection":
        pass

    def pages(self) -> Iterator[List["MultipartUpload"]]:
        pass

    def __iter__(self) -> Iterator["MultipartUpload"]:
        pass


class BucketObjectVersionsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.object_versions)
    [Show boto3-stubs documentation](./service_resource.md#bucketobjectversionscollection)
    """

    def all(self) -> "BucketObjectVersionsCollection":
        pass

    def filter(  # type: ignore
        self,
        Delimiter: str = None,
        EncodingType: Literal["url"] = None,
        KeyMarker: str = None,
        MaxKeys: int = None,
        Prefix: str = None,
        VersionIdMarker: str = None,
        ExpectedBucketOwner: str = None,
    ) -> "BucketObjectVersionsCollection":
        pass

    def delete(
        self,
        MFA: str = None,
        RequestPayer: Literal["requester"] = None,
        BypassGovernanceRetention: bool = None,
        ExpectedBucketOwner: str = None,
    ) -> DeleteObjectsOutputTypeDef:
        pass

    def limit(self, count: int) -> "BucketObjectVersionsCollection":
        pass

    def page_size(self, count: int) -> "BucketObjectVersionsCollection":
        pass

    def pages(self) -> Iterator[List["ObjectVersion"]]:
        pass

    def __iter__(self) -> Iterator["ObjectVersion"]:
        pass


class BucketObjectsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.objects)
    [Show boto3-stubs documentation](./service_resource.md#bucketobjectscollection)
    """

    def all(self) -> "BucketObjectsCollection":
        pass

    def filter(  # type: ignore
        self,
        Delimiter: str = None,
        EncodingType: Literal["url"] = None,
        Marker: str = None,
        MaxKeys: int = None,
        Prefix: str = None,
        RequestPayer: Literal["requester"] = None,
        ExpectedBucketOwner: str = None,
    ) -> "BucketObjectsCollection":
        pass

    def delete(
        self,
        MFA: str = None,
        RequestPayer: Literal["requester"] = None,
        BypassGovernanceRetention: bool = None,
        ExpectedBucketOwner: str = None,
    ) -> DeleteObjectsOutputTypeDef:
        pass

    def limit(self, count: int) -> "BucketObjectsCollection":
        pass

    def page_size(self, count: int) -> "BucketObjectsCollection":
        pass

    def pages(self) -> Iterator[List["ObjectSummary"]]:
        pass

    def __iter__(self) -> Iterator["ObjectSummary"]:
        pass


class MultipartUploadPartsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.MultipartUpload.parts)
    [Show boto3-stubs documentation](./service_resource.md#multipartuploadpartscollection)
    """

    def all(self) -> "MultipartUploadPartsCollection":
        pass

    def filter(  # type: ignore
        self,
        MaxParts: int = None,
        PartNumberMarker: int = None,
        RequestPayer: Literal["requester"] = None,
        ExpectedBucketOwner: str = None,
    ) -> "MultipartUploadPartsCollection":
        pass

    def limit(self, count: int) -> "MultipartUploadPartsCollection":
        pass

    def page_size(self, count: int) -> "MultipartUploadPartsCollection":
        pass

    def pages(self) -> Iterator[List["MultipartUploadPart"]]:
        pass

    def __iter__(self) -> Iterator["MultipartUploadPart"]:
        pass


class BucketAcl(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketAcl)[Show boto3-stubs documentation](./service_resource.md#bucketacl)
    """

    owner: Dict[str, Any]
    grants: List[Any]
    bucket_name: str

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketAcl.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#bucketaclbucketmethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketAcl.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#bucketaclget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketAcl.load)
        [Show boto3-stubs documentation](./service_resource.md#bucketaclloadmethod)
        """

    def put(
        self,
        ACL: BucketCannedACLType = None,
        AccessControlPolicy: AccessControlPolicyTypeDef = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWrite: str = None,
        GrantWriteACP: str = None,
        ExpectedBucketOwner: str = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketAcl.put)
        [Show boto3-stubs documentation](./service_resource.md#bucketaclputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketAcl.reload)
        [Show boto3-stubs documentation](./service_resource.md#bucketaclreloadmethod)
        """


_BucketAcl = BucketAcl


class BucketCors(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketCors)[Show boto3-stubs documentation](./service_resource.md#bucketcors)
    """

    cors_rules: List[Any]
    bucket_name: str

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketCors.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#bucketcorsbucketmethod)
        """

    def delete(self, ExpectedBucketOwner: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketCors.delete)
        [Show boto3-stubs documentation](./service_resource.md#bucketcorsdeletemethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketCors.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#bucketcorsget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketCors.load)
        [Show boto3-stubs documentation](./service_resource.md#bucketcorsloadmethod)
        """

    def put(
        self, CORSConfiguration: CORSConfigurationTypeDef, ExpectedBucketOwner: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketCors.put)
        [Show boto3-stubs documentation](./service_resource.md#bucketcorsputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketCors.reload)
        [Show boto3-stubs documentation](./service_resource.md#bucketcorsreloadmethod)
        """


_BucketCors = BucketCors


class BucketLifecycle(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketLifecycle)[Show boto3-stubs documentation](./service_resource.md#bucketlifecycle)
    """

    rules: List[Any]
    bucket_name: str

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLifecycle.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecyclebucketmethod)
        """

    def delete(self, ExpectedBucketOwner: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLifecycle.delete)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecycledeletemethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLifecycle.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecycleget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLifecycle.load)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecycleloadmethod)
        """

    def put(
        self,
        LifecycleConfiguration: LifecycleConfigurationTypeDef = None,
        ExpectedBucketOwner: str = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLifecycle.put)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecycleputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLifecycle.reload)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecyclereloadmethod)
        """


_BucketLifecycle = BucketLifecycle


class BucketLifecycleConfiguration(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketLifecycleConfiguration)[Show boto3-stubs documentation](./service_resource.md#bucketlifecycleconfiguration)
    """

    rules: List[Any]
    bucket_name: str

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLifecycleConfiguration.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecycleconfigurationbucketmethod)
        """

    def delete(self, ExpectedBucketOwner: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLifecycleConfiguration.delete)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecycleconfigurationdeletemethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLifecycleConfiguration.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecycleconfigurationget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLifecycleConfiguration.load)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecycleconfigurationloadmethod)
        """

    def put(
        self,
        LifecycleConfiguration: BucketLifecycleConfigurationTypeDef = None,
        ExpectedBucketOwner: str = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLifecycleConfiguration.put)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecycleconfigurationputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLifecycleConfiguration.reload)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecycleconfigurationreloadmethod)
        """


_BucketLifecycleConfiguration = BucketLifecycleConfiguration


class BucketLogging(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketLogging)[Show boto3-stubs documentation](./service_resource.md#bucketlogging)
    """

    logging_enabled: Dict[str, Any]
    bucket_name: str

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLogging.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#bucketloggingbucketmethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLogging.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#bucketloggingget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLogging.load)
        [Show boto3-stubs documentation](./service_resource.md#bucketloggingloadmethod)
        """

    def put(
        self, BucketLoggingStatus: BucketLoggingStatusTypeDef, ExpectedBucketOwner: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLogging.put)
        [Show boto3-stubs documentation](./service_resource.md#bucketloggingputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketLogging.reload)
        [Show boto3-stubs documentation](./service_resource.md#bucketloggingreloadmethod)
        """


_BucketLogging = BucketLogging


class BucketNotification(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketNotification)[Show boto3-stubs documentation](./service_resource.md#bucketnotification)
    """

    topic_configurations: List[Any]
    queue_configurations: List[Any]
    lambda_function_configurations: List[Any]
    bucket_name: str

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketNotification.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#bucketnotificationbucketmethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketNotification.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#bucketnotificationget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketNotification.load)
        [Show boto3-stubs documentation](./service_resource.md#bucketnotificationloadmethod)
        """

    def put(
        self,
        NotificationConfiguration: NotificationConfigurationTypeDef,
        ExpectedBucketOwner: str = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketNotification.put)
        [Show boto3-stubs documentation](./service_resource.md#bucketnotificationputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketNotification.reload)
        [Show boto3-stubs documentation](./service_resource.md#bucketnotificationreloadmethod)
        """


_BucketNotification = BucketNotification


class BucketPolicy(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketPolicy)[Show boto3-stubs documentation](./service_resource.md#bucketpolicy)
    """

    policy: str
    bucket_name: str

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketPolicy.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#bucketpolicybucketmethod)
        """

    def delete(self, ExpectedBucketOwner: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketPolicy.delete)
        [Show boto3-stubs documentation](./service_resource.md#bucketpolicydeletemethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketPolicy.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#bucketpolicyget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketPolicy.load)
        [Show boto3-stubs documentation](./service_resource.md#bucketpolicyloadmethod)
        """

    def put(
        self,
        Policy: str,
        ConfirmRemoveSelfBucketAccess: bool = None,
        ExpectedBucketOwner: str = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketPolicy.put)
        [Show boto3-stubs documentation](./service_resource.md#bucketpolicyputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketPolicy.reload)
        [Show boto3-stubs documentation](./service_resource.md#bucketpolicyreloadmethod)
        """


_BucketPolicy = BucketPolicy


class BucketRequestPayment(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketRequestPayment)[Show boto3-stubs documentation](./service_resource.md#bucketrequestpayment)
    """

    payer: str
    bucket_name: str

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketRequestPayment.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#bucketrequestpaymentbucketmethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketRequestPayment.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#bucketrequestpaymentget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketRequestPayment.load)
        [Show boto3-stubs documentation](./service_resource.md#bucketrequestpaymentloadmethod)
        """

    def put(
        self,
        RequestPaymentConfiguration: RequestPaymentConfigurationTypeDef,
        ExpectedBucketOwner: str = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketRequestPayment.put)
        [Show boto3-stubs documentation](./service_resource.md#bucketrequestpaymentputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketRequestPayment.reload)
        [Show boto3-stubs documentation](./service_resource.md#bucketrequestpaymentreloadmethod)
        """


_BucketRequestPayment = BucketRequestPayment


class BucketTagging(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketTagging)[Show boto3-stubs documentation](./service_resource.md#buckettagging)
    """

    tag_set: List[Any]
    bucket_name: str

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketTagging.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#buckettaggingbucketmethod)
        """

    def delete(self, ExpectedBucketOwner: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketTagging.delete)
        [Show boto3-stubs documentation](./service_resource.md#buckettaggingdeletemethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketTagging.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#buckettaggingget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketTagging.load)
        [Show boto3-stubs documentation](./service_resource.md#buckettaggingloadmethod)
        """

    def put(self, Tagging: "TaggingTypeDef", ExpectedBucketOwner: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketTagging.put)
        [Show boto3-stubs documentation](./service_resource.md#buckettaggingputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketTagging.reload)
        [Show boto3-stubs documentation](./service_resource.md#buckettaggingreloadmethod)
        """


_BucketTagging = BucketTagging


class BucketVersioning(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketVersioning)[Show boto3-stubs documentation](./service_resource.md#bucketversioning)
    """

    status: str
    mfa_delete: str
    bucket_name: str

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketVersioning.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#bucketversioningbucketmethod)
        """

    def enable(
        self,
        VersioningConfiguration: VersioningConfigurationTypeDef,
        MFA: str = None,
        ExpectedBucketOwner: str = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketVersioning.enable)
        [Show boto3-stubs documentation](./service_resource.md#bucketversioningenablemethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketVersioning.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#bucketversioningget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketVersioning.load)
        [Show boto3-stubs documentation](./service_resource.md#bucketversioningloadmethod)
        """

    def put(
        self,
        VersioningConfiguration: VersioningConfigurationTypeDef,
        MFA: str = None,
        ExpectedBucketOwner: str = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketVersioning.put)
        [Show boto3-stubs documentation](./service_resource.md#bucketversioningputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketVersioning.reload)
        [Show boto3-stubs documentation](./service_resource.md#bucketversioningreloadmethod)
        """

    def suspend(
        self,
        VersioningConfiguration: VersioningConfigurationTypeDef,
        MFA: str = None,
        ExpectedBucketOwner: str = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketVersioning.suspend)
        [Show boto3-stubs documentation](./service_resource.md#bucketversioningsuspendmethod)
        """


_BucketVersioning = BucketVersioning


class BucketWebsite(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketWebsite)[Show boto3-stubs documentation](./service_resource.md#bucketwebsite)
    """

    redirect_all_requests_to: Dict[str, Any]
    index_document: Dict[str, Any]
    error_document: Dict[str, Any]
    routing_rules: List[Any]
    bucket_name: str

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketWebsite.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#bucketwebsitebucketmethod)
        """

    def delete(self, ExpectedBucketOwner: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketWebsite.delete)
        [Show boto3-stubs documentation](./service_resource.md#bucketwebsitedeletemethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketWebsite.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#bucketwebsiteget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketWebsite.load)
        [Show boto3-stubs documentation](./service_resource.md#bucketwebsiteloadmethod)
        """

    def put(
        self, WebsiteConfiguration: WebsiteConfigurationTypeDef, ExpectedBucketOwner: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketWebsite.put)
        [Show boto3-stubs documentation](./service_resource.md#bucketwebsiteputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.BucketWebsite.reload)
        [Show boto3-stubs documentation](./service_resource.md#bucketwebsitereloadmethod)
        """


_BucketWebsite = BucketWebsite


class MultipartUploadPart(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.MultipartUploadPart)[Show boto3-stubs documentation](./service_resource.md#multipartuploadpart)
    """

    last_modified: datetime
    e_tag: str
    size: int
    bucket_name: str
    object_key: str
    multipart_upload_id: str
    part_number: str

    def MultipartUpload(self) -> "_MultipartUpload":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.MultipartUploadPart.MultipartUpload)
        [Show boto3-stubs documentation](./service_resource.md#multipartuploadpartmultipartuploadmethod)
        """

    def copy_from(
        self,
        CopySource: str,
        CopySourceIfMatch: str = None,
        CopySourceIfModifiedSince: datetime = None,
        CopySourceIfNoneMatch: str = None,
        CopySourceIfUnmodifiedSince: datetime = None,
        CopySourceRange: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        CopySourceSSECustomerAlgorithm: str = None,
        CopySourceSSECustomerKey: str = None,
        CopySourceSSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        ExpectedBucketOwner: str = None,
        ExpectedSourceBucketOwner: str = None,
    ) -> UploadPartCopyOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.MultipartUploadPart.copy_from)
        [Show boto3-stubs documentation](./service_resource.md#multipartuploadpartcopy_frommethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.MultipartUploadPart.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#multipartuploadpartget_available_subresourcesmethod)
        """

    def upload(
        self,
        Body: Union[bytes, IO[bytes]] = None,
        ContentLength: int = None,
        ContentMD5: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        ExpectedBucketOwner: str = None,
    ) -> UploadPartOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.MultipartUploadPart.upload)
        [Show boto3-stubs documentation](./service_resource.md#multipartuploadpartuploadmethod)
        """


_MultipartUploadPart = MultipartUploadPart


class ObjectAcl(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.ObjectAcl)[Show boto3-stubs documentation](./service_resource.md#objectacl)
    """

    owner: Dict[str, Any]
    grants: List[Any]
    request_charged: str
    bucket_name: str
    object_key: str

    def Object(self) -> "_Object":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectAcl.Object)
        [Show boto3-stubs documentation](./service_resource.md#objectaclobjectmethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectAcl.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#objectaclget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectAcl.load)
        [Show boto3-stubs documentation](./service_resource.md#objectaclloadmethod)
        """

    def put(
        self,
        ACL: ObjectCannedACLType = None,
        AccessControlPolicy: AccessControlPolicyTypeDef = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWrite: str = None,
        GrantWriteACP: str = None,
        RequestPayer: Literal["requester"] = None,
        VersionId: str = None,
        ExpectedBucketOwner: str = None,
    ) -> PutObjectAclOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectAcl.put)
        [Show boto3-stubs documentation](./service_resource.md#objectaclputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectAcl.reload)
        [Show boto3-stubs documentation](./service_resource.md#objectaclreloadmethod)
        """


_ObjectAcl = ObjectAcl


class ObjectVersion(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.ObjectVersion)[Show boto3-stubs documentation](./service_resource.md#objectversion)
    """

    e_tag: str
    size: int
    storage_class: str
    key: str
    version_id: str
    is_latest: bool
    last_modified: datetime
    owner: Dict[str, Any]
    bucket_name: str
    object_key: str
    id: str

    def Object(self) -> "_Object":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectVersion.Object)
        [Show boto3-stubs documentation](./service_resource.md#objectversionobjectmethod)
        """

    def delete(
        self,
        MFA: str = None,
        RequestPayer: Literal["requester"] = None,
        BypassGovernanceRetention: bool = None,
        ExpectedBucketOwner: str = None,
    ) -> DeleteObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectVersion.delete)
        [Show boto3-stubs documentation](./service_resource.md#objectversiondeletemethod)
        """

    def get(
        self,
        IfMatch: str = None,
        IfModifiedSince: datetime = None,
        IfNoneMatch: str = None,
        IfUnmodifiedSince: datetime = None,
        Range: str = None,
        ResponseCacheControl: str = None,
        ResponseContentDisposition: str = None,
        ResponseContentEncoding: str = None,
        ResponseContentLanguage: str = None,
        ResponseContentType: str = None,
        ResponseExpires: datetime = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        PartNumber: int = None,
        ExpectedBucketOwner: str = None,
    ) -> GetObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectVersion.get)
        [Show boto3-stubs documentation](./service_resource.md#objectversiongetmethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectVersion.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#objectversionget_available_subresourcesmethod)
        """

    def head(
        self,
        IfMatch: str = None,
        IfModifiedSince: datetime = None,
        IfNoneMatch: str = None,
        IfUnmodifiedSince: datetime = None,
        Range: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        PartNumber: int = None,
        ExpectedBucketOwner: str = None,
    ) -> HeadObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectVersion.head)
        [Show boto3-stubs documentation](./service_resource.md#objectversionheadmethod)
        """


_ObjectVersion = ObjectVersion


class MultipartUpload(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.MultipartUpload)[Show boto3-stubs documentation](./service_resource.md#multipartupload)
    """

    upload_id: str
    key: str
    initiated: datetime
    storage_class: str
    owner: Dict[str, Any]
    initiator: Dict[str, Any]
    bucket_name: str
    object_key: str
    id: str
    parts: MultipartUploadPartsCollection

    def Object(self) -> "_Object":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.MultipartUpload.Object)
        [Show boto3-stubs documentation](./service_resource.md#multipartuploadobjectmethod)
        """

    def Part(self, part_number: str) -> _MultipartUploadPart:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.MultipartUpload.Part)
        [Show boto3-stubs documentation](./service_resource.md#multipartuploadpartmethod)
        """

    def abort(
        self, RequestPayer: Literal["requester"] = None, ExpectedBucketOwner: str = None
    ) -> AbortMultipartUploadOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.MultipartUpload.abort)
        [Show boto3-stubs documentation](./service_resource.md#multipartuploadabortmethod)
        """

    def complete(
        self,
        MultipartUpload: CompletedMultipartUploadTypeDef = None,
        RequestPayer: Literal["requester"] = None,
        ExpectedBucketOwner: str = None,
    ) -> "_Object":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.MultipartUpload.complete)
        [Show boto3-stubs documentation](./service_resource.md#multipartuploadcompletemethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.MultipartUpload.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#multipartuploadget_available_subresourcesmethod)
        """


_MultipartUpload = MultipartUpload


class Object(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.Object)[Show boto3-stubs documentation](./service_resource.md#object)
    """

    delete_marker: bool
    accept_ranges: str
    expiration: str
    restore: str
    archive_status: str
    last_modified: datetime
    content_length: int
    e_tag: str
    missing_meta: int
    version_id: str
    cache_control: str
    content_disposition: str
    content_encoding: str
    content_language: str
    content_type: str
    expires: datetime
    website_redirect_location: str
    server_side_encryption: str
    metadata: Dict[str, Any]
    sse_customer_algorithm: str
    sse_customer_key_md5: str
    ssekms_key_id: str
    bucket_key_enabled: bool
    storage_class: str
    request_charged: str
    replication_status: str
    parts_count: int
    object_lock_mode: str
    object_lock_retain_until_date: datetime
    object_lock_legal_hold_status: str
    bucket_name: str
    key: str

    def Acl(self) -> _ObjectAcl:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.Acl)
        [Show boto3-stubs documentation](./service_resource.md#objectaclmethod)
        """

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#objectbucketmethod)
        """

    def MultipartUpload(self, id: str) -> _MultipartUpload:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.MultipartUpload)
        [Show boto3-stubs documentation](./service_resource.md#objectmultipartuploadmethod)
        """

    def Version(self, id: str) -> _ObjectVersion:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.Version)
        [Show boto3-stubs documentation](./service_resource.md#objectversionmethod)
        """

    def copy(
        self,
        CopySource: CopySourceTypeDef,
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        SourceClient: BaseClient = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.copy)
        [Show boto3-stubs documentation](./service_resource.md#objectcopymethod)
        """

    def copy_from(
        self,
        CopySource: str,
        ACL: ObjectCannedACLType = None,
        CacheControl: str = None,
        ContentDisposition: str = None,
        ContentEncoding: str = None,
        ContentLanguage: str = None,
        ContentType: str = None,
        CopySourceIfMatch: str = None,
        CopySourceIfModifiedSince: datetime = None,
        CopySourceIfNoneMatch: str = None,
        CopySourceIfUnmodifiedSince: datetime = None,
        Expires: datetime = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWriteACP: str = None,
        Metadata: Dict[str, str] = None,
        MetadataDirective: MetadataDirectiveType = None,
        TaggingDirective: TaggingDirectiveType = None,
        ServerSideEncryption: ServerSideEncryptionType = None,
        StorageClass: StorageClassType = None,
        WebsiteRedirectLocation: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        SSEKMSKeyId: str = None,
        SSEKMSEncryptionContext: str = None,
        BucketKeyEnabled: bool = None,
        CopySourceSSECustomerAlgorithm: str = None,
        CopySourceSSECustomerKey: str = None,
        CopySourceSSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        Tagging: str = None,
        ObjectLockMode: ObjectLockModeType = None,
        ObjectLockRetainUntilDate: datetime = None,
        ObjectLockLegalHoldStatus: ObjectLockLegalHoldStatusType = None,
        ExpectedBucketOwner: str = None,
        ExpectedSourceBucketOwner: str = None,
    ) -> CopyObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.copy_from)
        [Show boto3-stubs documentation](./service_resource.md#objectcopy_frommethod)
        """

    def delete(
        self,
        MFA: str = None,
        VersionId: str = None,
        RequestPayer: Literal["requester"] = None,
        BypassGovernanceRetention: bool = None,
        ExpectedBucketOwner: str = None,
    ) -> DeleteObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.delete)
        [Show boto3-stubs documentation](./service_resource.md#objectdeletemethod)
        """

    def download_file(
        self,
        Filename: str,
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.download_file)
        [Show boto3-stubs documentation](./service_resource.md#objectdownload_filemethod)
        """

    def download_fileobj(
        self,
        Fileobj: IO[Any],
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.download_fileobj)
        [Show boto3-stubs documentation](./service_resource.md#objectdownload_fileobjmethod)
        """

    def get(
        self,
        IfMatch: str = None,
        IfModifiedSince: datetime = None,
        IfNoneMatch: str = None,
        IfUnmodifiedSince: datetime = None,
        Range: str = None,
        ResponseCacheControl: str = None,
        ResponseContentDisposition: str = None,
        ResponseContentEncoding: str = None,
        ResponseContentLanguage: str = None,
        ResponseContentType: str = None,
        ResponseExpires: datetime = None,
        VersionId: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        PartNumber: int = None,
        ExpectedBucketOwner: str = None,
    ) -> GetObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.get)
        [Show boto3-stubs documentation](./service_resource.md#objectgetmethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#objectget_available_subresourcesmethod)
        """

    def initiate_multipart_upload(
        self,
        ACL: ObjectCannedACLType = None,
        CacheControl: str = None,
        ContentDisposition: str = None,
        ContentEncoding: str = None,
        ContentLanguage: str = None,
        ContentType: str = None,
        Expires: datetime = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWriteACP: str = None,
        Metadata: Dict[str, str] = None,
        ServerSideEncryption: ServerSideEncryptionType = None,
        StorageClass: StorageClassType = None,
        WebsiteRedirectLocation: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        SSEKMSKeyId: str = None,
        SSEKMSEncryptionContext: str = None,
        BucketKeyEnabled: bool = None,
        RequestPayer: Literal["requester"] = None,
        Tagging: str = None,
        ObjectLockMode: ObjectLockModeType = None,
        ObjectLockRetainUntilDate: datetime = None,
        ObjectLockLegalHoldStatus: ObjectLockLegalHoldStatusType = None,
        ExpectedBucketOwner: str = None,
    ) -> _MultipartUpload:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.initiate_multipart_upload)
        [Show boto3-stubs documentation](./service_resource.md#objectinitiate_multipart_uploadmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.load)
        [Show boto3-stubs documentation](./service_resource.md#objectloadmethod)
        """

    def put(
        self,
        ACL: ObjectCannedACLType = None,
        Body: Union[bytes, IO[bytes]] = None,
        CacheControl: str = None,
        ContentDisposition: str = None,
        ContentEncoding: str = None,
        ContentLanguage: str = None,
        ContentLength: int = None,
        ContentMD5: str = None,
        ContentType: str = None,
        Expires: datetime = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWriteACP: str = None,
        Metadata: Dict[str, str] = None,
        ServerSideEncryption: ServerSideEncryptionType = None,
        StorageClass: StorageClassType = None,
        WebsiteRedirectLocation: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        SSEKMSKeyId: str = None,
        SSEKMSEncryptionContext: str = None,
        BucketKeyEnabled: bool = None,
        RequestPayer: Literal["requester"] = None,
        Tagging: str = None,
        ObjectLockMode: ObjectLockModeType = None,
        ObjectLockRetainUntilDate: datetime = None,
        ObjectLockLegalHoldStatus: ObjectLockLegalHoldStatusType = None,
        ExpectedBucketOwner: str = None,
    ) -> PutObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.put)
        [Show boto3-stubs documentation](./service_resource.md#objectputmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.reload)
        [Show boto3-stubs documentation](./service_resource.md#objectreloadmethod)
        """

    def restore_object(
        self,
        VersionId: str = None,
        RestoreRequest: RestoreRequestTypeDef = None,
        RequestPayer: Literal["requester"] = None,
        ExpectedBucketOwner: str = None,
    ) -> RestoreObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.restore_object)
        [Show boto3-stubs documentation](./service_resource.md#objectrestore_objectmethod)
        """

    def upload_file(
        self,
        Filename: str,
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.upload_file)
        [Show boto3-stubs documentation](./service_resource.md#objectupload_filemethod)
        """

    def upload_fileobj(
        self,
        Fileobj: IO[Any],
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.upload_fileobj)
        [Show boto3-stubs documentation](./service_resource.md#objectupload_fileobjmethod)
        """

    def wait_until_exists(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.wait_until_exists)
        [Show boto3-stubs documentation](./service_resource.md#objectwait_until_existsmethod)
        """

    def wait_until_not_exists(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Object.wait_until_not_exists)
        [Show boto3-stubs documentation](./service_resource.md#objectwait_until_not_existsmethod)
        """


_Object = Object


class ObjectSummary(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.ObjectSummary)[Show boto3-stubs documentation](./service_resource.md#objectsummary)
    """

    last_modified: datetime
    e_tag: str
    size: int
    storage_class: str
    owner: Dict[str, Any]
    bucket_name: str
    key: str

    def Acl(self) -> _ObjectAcl:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.Acl)
        [Show boto3-stubs documentation](./service_resource.md#objectsummaryaclmethod)
        """

    def Bucket(self) -> "_Bucket":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#objectsummarybucketmethod)
        """

    def MultipartUpload(self, id: str) -> _MultipartUpload:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.MultipartUpload)
        [Show boto3-stubs documentation](./service_resource.md#objectsummarymultipartuploadmethod)
        """

    def Object(self) -> _Object:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.Object)
        [Show boto3-stubs documentation](./service_resource.md#objectsummaryobjectmethod)
        """

    def Version(self, id: str) -> _ObjectVersion:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.Version)
        [Show boto3-stubs documentation](./service_resource.md#objectsummaryversionmethod)
        """

    def copy_from(
        self,
        CopySource: str,
        ACL: ObjectCannedACLType = None,
        CacheControl: str = None,
        ContentDisposition: str = None,
        ContentEncoding: str = None,
        ContentLanguage: str = None,
        ContentType: str = None,
        CopySourceIfMatch: str = None,
        CopySourceIfModifiedSince: datetime = None,
        CopySourceIfNoneMatch: str = None,
        CopySourceIfUnmodifiedSince: datetime = None,
        Expires: datetime = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWriteACP: str = None,
        Metadata: Dict[str, str] = None,
        MetadataDirective: MetadataDirectiveType = None,
        TaggingDirective: TaggingDirectiveType = None,
        ServerSideEncryption: ServerSideEncryptionType = None,
        StorageClass: StorageClassType = None,
        WebsiteRedirectLocation: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        SSEKMSKeyId: str = None,
        SSEKMSEncryptionContext: str = None,
        BucketKeyEnabled: bool = None,
        CopySourceSSECustomerAlgorithm: str = None,
        CopySourceSSECustomerKey: str = None,
        CopySourceSSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        Tagging: str = None,
        ObjectLockMode: ObjectLockModeType = None,
        ObjectLockRetainUntilDate: datetime = None,
        ObjectLockLegalHoldStatus: ObjectLockLegalHoldStatusType = None,
        ExpectedBucketOwner: str = None,
        ExpectedSourceBucketOwner: str = None,
    ) -> CopyObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.copy_from)
        [Show boto3-stubs documentation](./service_resource.md#objectsummarycopy_frommethod)
        """

    def delete(
        self,
        MFA: str = None,
        VersionId: str = None,
        RequestPayer: Literal["requester"] = None,
        BypassGovernanceRetention: bool = None,
        ExpectedBucketOwner: str = None,
    ) -> DeleteObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.delete)
        [Show boto3-stubs documentation](./service_resource.md#objectsummarydeletemethod)
        """

    def get(
        self,
        IfMatch: str = None,
        IfModifiedSince: datetime = None,
        IfNoneMatch: str = None,
        IfUnmodifiedSince: datetime = None,
        Range: str = None,
        ResponseCacheControl: str = None,
        ResponseContentDisposition: str = None,
        ResponseContentEncoding: str = None,
        ResponseContentLanguage: str = None,
        ResponseContentType: str = None,
        ResponseExpires: datetime = None,
        VersionId: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        PartNumber: int = None,
        ExpectedBucketOwner: str = None,
    ) -> GetObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.get)
        [Show boto3-stubs documentation](./service_resource.md#objectsummarygetmethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#objectsummaryget_available_subresourcesmethod)
        """

    def initiate_multipart_upload(
        self,
        ACL: ObjectCannedACLType = None,
        CacheControl: str = None,
        ContentDisposition: str = None,
        ContentEncoding: str = None,
        ContentLanguage: str = None,
        ContentType: str = None,
        Expires: datetime = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWriteACP: str = None,
        Metadata: Dict[str, str] = None,
        ServerSideEncryption: ServerSideEncryptionType = None,
        StorageClass: StorageClassType = None,
        WebsiteRedirectLocation: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        SSEKMSKeyId: str = None,
        SSEKMSEncryptionContext: str = None,
        BucketKeyEnabled: bool = None,
        RequestPayer: Literal["requester"] = None,
        Tagging: str = None,
        ObjectLockMode: ObjectLockModeType = None,
        ObjectLockRetainUntilDate: datetime = None,
        ObjectLockLegalHoldStatus: ObjectLockLegalHoldStatusType = None,
        ExpectedBucketOwner: str = None,
    ) -> _MultipartUpload:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.initiate_multipart_upload)
        [Show boto3-stubs documentation](./service_resource.md#objectsummaryinitiate_multipart_uploadmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.load)
        [Show boto3-stubs documentation](./service_resource.md#objectsummaryloadmethod)
        """

    def put(
        self,
        ACL: ObjectCannedACLType = None,
        Body: Union[bytes, IO[bytes]] = None,
        CacheControl: str = None,
        ContentDisposition: str = None,
        ContentEncoding: str = None,
        ContentLanguage: str = None,
        ContentLength: int = None,
        ContentMD5: str = None,
        ContentType: str = None,
        Expires: datetime = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWriteACP: str = None,
        Metadata: Dict[str, str] = None,
        ServerSideEncryption: ServerSideEncryptionType = None,
        StorageClass: StorageClassType = None,
        WebsiteRedirectLocation: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        SSEKMSKeyId: str = None,
        SSEKMSEncryptionContext: str = None,
        BucketKeyEnabled: bool = None,
        RequestPayer: Literal["requester"] = None,
        Tagging: str = None,
        ObjectLockMode: ObjectLockModeType = None,
        ObjectLockRetainUntilDate: datetime = None,
        ObjectLockLegalHoldStatus: ObjectLockLegalHoldStatusType = None,
        ExpectedBucketOwner: str = None,
    ) -> PutObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.put)
        [Show boto3-stubs documentation](./service_resource.md#objectsummaryputmethod)
        """

    def restore_object(
        self,
        VersionId: str = None,
        RestoreRequest: RestoreRequestTypeDef = None,
        RequestPayer: Literal["requester"] = None,
        ExpectedBucketOwner: str = None,
    ) -> RestoreObjectOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.restore_object)
        [Show boto3-stubs documentation](./service_resource.md#objectsummaryrestore_objectmethod)
        """

    def wait_until_exists(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.wait_until_exists)
        [Show boto3-stubs documentation](./service_resource.md#objectsummarywait_until_existsmethod)
        """

    def wait_until_not_exists(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ObjectSummary.wait_until_not_exists)
        [Show boto3-stubs documentation](./service_resource.md#objectsummarywait_until_not_existsmethod)
        """


_ObjectSummary = ObjectSummary


class Bucket(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.Bucket)[Show boto3-stubs documentation](./service_resource.md#bucket)
    """

    creation_date: datetime
    name: str
    multipart_uploads: BucketMultipartUploadsCollection
    object_versions: BucketObjectVersionsCollection
    objects: BucketObjectsCollection

    def Acl(self) -> _BucketAcl:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.Acl)
        [Show boto3-stubs documentation](./service_resource.md#bucketaclmethod)
        """

    def Cors(self) -> _BucketCors:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.Cors)
        [Show boto3-stubs documentation](./service_resource.md#bucketcorsmethod)
        """

    def Lifecycle(self) -> _BucketLifecycle:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.Lifecycle)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecyclemethod)
        """

    def LifecycleConfiguration(self) -> _BucketLifecycleConfiguration:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.LifecycleConfiguration)
        [Show boto3-stubs documentation](./service_resource.md#bucketlifecycleconfigurationmethod)
        """

    def Logging(self) -> _BucketLogging:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.Logging)
        [Show boto3-stubs documentation](./service_resource.md#bucketloggingmethod)
        """

    def Notification(self) -> _BucketNotification:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.Notification)
        [Show boto3-stubs documentation](./service_resource.md#bucketnotificationmethod)
        """

    def Object(self, key: str) -> _Object:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.Object)
        [Show boto3-stubs documentation](./service_resource.md#bucketobjectmethod)
        """

    def Policy(self) -> _BucketPolicy:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.Policy)
        [Show boto3-stubs documentation](./service_resource.md#bucketpolicymethod)
        """

    def RequestPayment(self) -> _BucketRequestPayment:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.RequestPayment)
        [Show boto3-stubs documentation](./service_resource.md#bucketrequestpaymentmethod)
        """

    def Tagging(self) -> _BucketTagging:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.Tagging)
        [Show boto3-stubs documentation](./service_resource.md#buckettaggingmethod)
        """

    def Versioning(self) -> _BucketVersioning:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.Versioning)
        [Show boto3-stubs documentation](./service_resource.md#bucketversioningmethod)
        """

    def Website(self) -> _BucketWebsite:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.Website)
        [Show boto3-stubs documentation](./service_resource.md#bucketwebsitemethod)
        """

    def copy(
        self,
        CopySource: CopySourceTypeDef,
        Key: str,
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        SourceClient: BaseClient = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.copy)
        [Show boto3-stubs documentation](./service_resource.md#bucketcopymethod)
        """

    def create(
        self,
        ACL: BucketCannedACLType = None,
        CreateBucketConfiguration: CreateBucketConfigurationTypeDef = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWrite: str = None,
        GrantWriteACP: str = None,
        ObjectLockEnabledForBucket: bool = None,
    ) -> CreateBucketOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.create)
        [Show boto3-stubs documentation](./service_resource.md#bucketcreatemethod)
        """

    def delete(self, ExpectedBucketOwner: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.delete)
        [Show boto3-stubs documentation](./service_resource.md#bucketdeletemethod)
        """

    def delete_objects(
        self,
        Delete: DeleteTypeDef,
        MFA: str = None,
        RequestPayer: Literal["requester"] = None,
        BypassGovernanceRetention: bool = None,
        ExpectedBucketOwner: str = None,
    ) -> DeleteObjectsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.delete_objects)
        [Show boto3-stubs documentation](./service_resource.md#bucketdelete_objectsmethod)
        """

    def download_file(
        self,
        Key: str,
        Filename: str,
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.download_file)
        [Show boto3-stubs documentation](./service_resource.md#bucketdownload_filemethod)
        """

    def download_fileobj(
        self,
        Key: str,
        Fileobj: IO[Any],
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.download_fileobj)
        [Show boto3-stubs documentation](./service_resource.md#bucketdownload_fileobjmethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#bucketget_available_subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.load)
        [Show boto3-stubs documentation](./service_resource.md#bucketloadmethod)
        """

    def put_object(
        self,
        Key: str,
        ACL: ObjectCannedACLType = None,
        Body: Union[bytes, IO[bytes]] = None,
        CacheControl: str = None,
        ContentDisposition: str = None,
        ContentEncoding: str = None,
        ContentLanguage: str = None,
        ContentLength: int = None,
        ContentMD5: str = None,
        ContentType: str = None,
        Expires: datetime = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWriteACP: str = None,
        Metadata: Dict[str, str] = None,
        ServerSideEncryption: ServerSideEncryptionType = None,
        StorageClass: StorageClassType = None,
        WebsiteRedirectLocation: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        SSEKMSKeyId: str = None,
        SSEKMSEncryptionContext: str = None,
        BucketKeyEnabled: bool = None,
        RequestPayer: Literal["requester"] = None,
        Tagging: str = None,
        ObjectLockMode: ObjectLockModeType = None,
        ObjectLockRetainUntilDate: datetime = None,
        ObjectLockLegalHoldStatus: ObjectLockLegalHoldStatusType = None,
        ExpectedBucketOwner: str = None,
    ) -> _Object:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.put_object)
        [Show boto3-stubs documentation](./service_resource.md#bucketput_objectmethod)
        """

    def upload_file(
        self,
        Filename: str,
        Key: str,
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.upload_file)
        [Show boto3-stubs documentation](./service_resource.md#bucketupload_filemethod)
        """

    def upload_fileobj(
        self,
        Fileobj: IO[Any],
        Key: str,
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.upload_fileobj)
        [Show boto3-stubs documentation](./service_resource.md#bucketupload_fileobjmethod)
        """

    def wait_until_exists(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.wait_until_exists)
        [Show boto3-stubs documentation](./service_resource.md#bucketwait_until_existsmethod)
        """

    def wait_until_not_exists(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.Bucket.wait_until_not_exists)
        [Show boto3-stubs documentation](./service_resource.md#bucketwait_until_not_existsmethod)
        """


_Bucket = Bucket


class S3ServiceResource(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource)[Show boto3-stubs documentation](./service_resource.md)
    """

    buckets: ServiceResourceBucketsCollection

    def Bucket(self, name: str) -> _Bucket:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.Bucket)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcebucketmethod)
        """

    def BucketAcl(self, bucket_name: str) -> _BucketAcl:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketAcl)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcebucketaclmethod)
        """

    def BucketCors(self, bucket_name: str) -> _BucketCors:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketCors)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcebucketcorsmethod)
        """

    def BucketLifecycle(self, bucket_name: str) -> _BucketLifecycle:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketLifecycle)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcebucketlifecyclemethod)
        """

    def BucketLifecycleConfiguration(self, bucket_name: str) -> _BucketLifecycleConfiguration:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketLifecycleConfiguration)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcebucketlifecycleconfigurationmethod)
        """

    def BucketLogging(self, bucket_name: str) -> _BucketLogging:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketLogging)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcebucketloggingmethod)
        """

    def BucketNotification(self, bucket_name: str) -> _BucketNotification:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketNotification)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcebucketnotificationmethod)
        """

    def BucketPolicy(self, bucket_name: str) -> _BucketPolicy:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketPolicy)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcebucketpolicymethod)
        """

    def BucketRequestPayment(self, bucket_name: str) -> _BucketRequestPayment:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketRequestPayment)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcebucketrequestpaymentmethod)
        """

    def BucketTagging(self, bucket_name: str) -> _BucketTagging:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketTagging)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcebuckettaggingmethod)
        """

    def BucketVersioning(self, bucket_name: str) -> _BucketVersioning:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketVersioning)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcebucketversioningmethod)
        """

    def BucketWebsite(self, bucket_name: str) -> _BucketWebsite:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.BucketWebsite)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcebucketwebsitemethod)
        """

    def MultipartUpload(self, bucket_name: str, object_key: str, id: str) -> _MultipartUpload:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.MultipartUpload)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcemultipartuploadmethod)
        """

    def MultipartUploadPart(
        self, bucket_name: str, object_key: str, multipart_upload_id: str, part_number: str
    ) -> _MultipartUploadPart:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.MultipartUploadPart)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcemultipartuploadpartmethod)
        """

    def Object(self, bucket_name: str, key: str) -> _Object:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.Object)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourceobjectmethod)
        """

    def ObjectAcl(self, bucket_name: str, object_key: str) -> _ObjectAcl:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.ObjectAcl)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourceobjectaclmethod)
        """

    def ObjectSummary(self, bucket_name: str, key: str) -> _ObjectSummary:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.ObjectSummary)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourceobjectsummarymethod)
        """

    def ObjectVersion(self, bucket_name: str, object_key: str, id: str) -> _ObjectVersion:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.ObjectVersion)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourceobjectversionmethod)
        """

    def create_bucket(
        self,
        Bucket: str,
        ACL: BucketCannedACLType = None,
        CreateBucketConfiguration: CreateBucketConfigurationTypeDef = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWrite: str = None,
        GrantWriteACP: str = None,
        ObjectLockEnabledForBucket: bool = None,
    ) -> _Bucket:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.create_bucket)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourcecreate_bucketmethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/s3.html#S3.ServiceResource.get_available_subresources)
        [Show boto3-stubs documentation](./service_resource.md#s3serviceresourceget_available_subresourcesmethod)
        """
