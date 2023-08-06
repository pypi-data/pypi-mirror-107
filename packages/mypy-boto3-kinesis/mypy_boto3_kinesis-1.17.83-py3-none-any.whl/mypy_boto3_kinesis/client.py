"""
Type annotations for kinesis service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_kinesis import KinesisClient

    client: KinesisClient = boto3.client("kinesis")
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Type, Union, overload

from botocore.client import ClientMeta

from .literals import EncryptionTypeType, MetricsNameType, ShardIteratorTypeType
from .paginator import (
    DescribeStreamPaginator,
    ListShardsPaginator,
    ListStreamConsumersPaginator,
    ListStreamsPaginator,
)
from .type_defs import (
    DescribeLimitsOutputTypeDef,
    DescribeStreamConsumerOutputTypeDef,
    DescribeStreamOutputTypeDef,
    DescribeStreamSummaryOutputTypeDef,
    EnhancedMonitoringOutputTypeDef,
    GetRecordsOutputTypeDef,
    GetShardIteratorOutputTypeDef,
    ListShardsOutputTypeDef,
    ListStreamConsumersOutputTypeDef,
    ListStreamsOutputTypeDef,
    ListTagsForStreamOutputTypeDef,
    PutRecordOutputTypeDef,
    PutRecordsOutputTypeDef,
    PutRecordsRequestEntryTypeDef,
    RegisterStreamConsumerOutputTypeDef,
    ShardFilterTypeDef,
    StartingPositionTypeDef,
    SubscribeToShardOutputTypeDef,
    UpdateShardCountOutputTypeDef,
)
from .waiter import StreamExistsWaiter, StreamNotExistsWaiter

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("KinesisClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ExpiredIteratorException: Type[BotocoreClientError]
    ExpiredNextTokenException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    KMSAccessDeniedException: Type[BotocoreClientError]
    KMSDisabledException: Type[BotocoreClientError]
    KMSInvalidStateException: Type[BotocoreClientError]
    KMSNotFoundException: Type[BotocoreClientError]
    KMSOptInRequired: Type[BotocoreClientError]
    KMSThrottlingException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ProvisionedThroughputExceededException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class KinesisClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def add_tags_to_stream(self, StreamName: str, Tags: Dict[str, str]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.add_tags_to_stream)
        [Show boto3-stubs documentation](./client.md#add_tags_to_stream)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can_paginate)
        """

    def create_stream(self, StreamName: str, ShardCount: int) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.create_stream)
        [Show boto3-stubs documentation](./client.md#create_stream)
        """

    def decrease_stream_retention_period(self, StreamName: str, RetentionPeriodHours: int) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.decrease_stream_retention_period)
        [Show boto3-stubs documentation](./client.md#decrease_stream_retention_period)
        """

    def delete_stream(self, StreamName: str, EnforceConsumerDeletion: bool = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.delete_stream)
        [Show boto3-stubs documentation](./client.md#delete_stream)
        """

    def deregister_stream_consumer(
        self, StreamARN: str = None, ConsumerName: str = None, ConsumerARN: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.deregister_stream_consumer)
        [Show boto3-stubs documentation](./client.md#deregister_stream_consumer)
        """

    def describe_limits(self) -> DescribeLimitsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.describe_limits)
        [Show boto3-stubs documentation](./client.md#describe_limits)
        """

    def describe_stream(
        self, StreamName: str, Limit: int = None, ExclusiveStartShardId: str = None
    ) -> DescribeStreamOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.describe_stream)
        [Show boto3-stubs documentation](./client.md#describe_stream)
        """

    def describe_stream_consumer(
        self, StreamARN: str = None, ConsumerName: str = None, ConsumerARN: str = None
    ) -> DescribeStreamConsumerOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.describe_stream_consumer)
        [Show boto3-stubs documentation](./client.md#describe_stream_consumer)
        """

    def describe_stream_summary(self, StreamName: str) -> DescribeStreamSummaryOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.describe_stream_summary)
        [Show boto3-stubs documentation](./client.md#describe_stream_summary)
        """

    def disable_enhanced_monitoring(
        self, StreamName: str, ShardLevelMetrics: List[MetricsNameType]
    ) -> EnhancedMonitoringOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.disable_enhanced_monitoring)
        [Show boto3-stubs documentation](./client.md#disable_enhanced_monitoring)
        """

    def enable_enhanced_monitoring(
        self, StreamName: str, ShardLevelMetrics: List[MetricsNameType]
    ) -> EnhancedMonitoringOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.enable_enhanced_monitoring)
        [Show boto3-stubs documentation](./client.md#enable_enhanced_monitoring)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate_presigned_url)
        """

    def get_records(self, ShardIterator: str, Limit: int = None) -> GetRecordsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.get_records)
        [Show boto3-stubs documentation](./client.md#get_records)
        """

    def get_shard_iterator(
        self,
        StreamName: str,
        ShardId: str,
        ShardIteratorType: ShardIteratorTypeType,
        StartingSequenceNumber: str = None,
        Timestamp: datetime = None,
    ) -> GetShardIteratorOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.get_shard_iterator)
        [Show boto3-stubs documentation](./client.md#get_shard_iterator)
        """

    def increase_stream_retention_period(self, StreamName: str, RetentionPeriodHours: int) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.increase_stream_retention_period)
        [Show boto3-stubs documentation](./client.md#increase_stream_retention_period)
        """

    def list_shards(
        self,
        StreamName: str = None,
        NextToken: str = None,
        ExclusiveStartShardId: str = None,
        MaxResults: int = None,
        StreamCreationTimestamp: datetime = None,
        ShardFilter: ShardFilterTypeDef = None,
    ) -> ListShardsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.list_shards)
        [Show boto3-stubs documentation](./client.md#list_shards)
        """

    def list_stream_consumers(
        self,
        StreamARN: str,
        NextToken: str = None,
        MaxResults: int = None,
        StreamCreationTimestamp: datetime = None,
    ) -> ListStreamConsumersOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.list_stream_consumers)
        [Show boto3-stubs documentation](./client.md#list_stream_consumers)
        """

    def list_streams(
        self, Limit: int = None, ExclusiveStartStreamName: str = None
    ) -> ListStreamsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.list_streams)
        [Show boto3-stubs documentation](./client.md#list_streams)
        """

    def list_tags_for_stream(
        self, StreamName: str, ExclusiveStartTagKey: str = None, Limit: int = None
    ) -> ListTagsForStreamOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.list_tags_for_stream)
        [Show boto3-stubs documentation](./client.md#list_tags_for_stream)
        """

    def merge_shards(self, StreamName: str, ShardToMerge: str, AdjacentShardToMerge: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.merge_shards)
        [Show boto3-stubs documentation](./client.md#merge_shards)
        """

    def put_record(
        self,
        StreamName: str,
        Data: Union[bytes, IO[bytes]],
        PartitionKey: str,
        ExplicitHashKey: str = None,
        SequenceNumberForOrdering: str = None,
    ) -> PutRecordOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.put_record)
        [Show boto3-stubs documentation](./client.md#put_record)
        """

    def put_records(
        self, Records: List[PutRecordsRequestEntryTypeDef], StreamName: str
    ) -> PutRecordsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.put_records)
        [Show boto3-stubs documentation](./client.md#put_records)
        """

    def register_stream_consumer(
        self, StreamARN: str, ConsumerName: str
    ) -> RegisterStreamConsumerOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.register_stream_consumer)
        [Show boto3-stubs documentation](./client.md#register_stream_consumer)
        """

    def remove_tags_from_stream(self, StreamName: str, TagKeys: List[str]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.remove_tags_from_stream)
        [Show boto3-stubs documentation](./client.md#remove_tags_from_stream)
        """

    def split_shard(self, StreamName: str, ShardToSplit: str, NewStartingHashKey: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.split_shard)
        [Show boto3-stubs documentation](./client.md#split_shard)
        """

    def start_stream_encryption(
        self, StreamName: str, EncryptionType: EncryptionTypeType, KeyId: str
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.start_stream_encryption)
        [Show boto3-stubs documentation](./client.md#start_stream_encryption)
        """

    def stop_stream_encryption(
        self, StreamName: str, EncryptionType: EncryptionTypeType, KeyId: str
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.stop_stream_encryption)
        [Show boto3-stubs documentation](./client.md#stop_stream_encryption)
        """

    def subscribe_to_shard(
        self, ConsumerARN: str, ShardId: str, StartingPosition: StartingPositionTypeDef
    ) -> SubscribeToShardOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.subscribe_to_shard)
        [Show boto3-stubs documentation](./client.md#subscribe_to_shard)
        """

    def update_shard_count(
        self, StreamName: str, TargetShardCount: int, ScalingType: Literal["UNIFORM_SCALING"]
    ) -> UpdateShardCountOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Client.update_shard_count)
        [Show boto3-stubs documentation](./client.md#update_shard_count)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_stream"]) -> DescribeStreamPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Paginator.DescribeStream)[Show boto3-stubs documentation](./paginators.md#describestreampaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_shards"]) -> ListShardsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Paginator.ListShards)[Show boto3-stubs documentation](./paginators.md#listshardspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_stream_consumers"]
    ) -> ListStreamConsumersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Paginator.ListStreamConsumers)[Show boto3-stubs documentation](./paginators.md#liststreamconsumerspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_streams"]) -> ListStreamsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Paginator.ListStreams)[Show boto3-stubs documentation](./paginators.md#liststreamspaginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["stream_exists"]) -> StreamExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Waiter.stream_exists)[Show boto3-stubs documentation](./waiters.md#streamexistswaiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["stream_not_exists"]) -> StreamNotExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/kinesis.html#Kinesis.Waiter.stream_not_exists)[Show boto3-stubs documentation](./waiters.md#streamnotexistswaiter)
        """
