"""
Type annotations for iotanalytics service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_iotanalytics import IoTAnalyticsClient

    client: IoTAnalyticsClient = boto3.client("iotanalytics")
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Type, Union, overload

from botocore.client import ClientMeta

from .paginator import (
    ListChannelsPaginator,
    ListDatasetContentsPaginator,
    ListDatasetsPaginator,
    ListDatastoresPaginator,
    ListPipelinesPaginator,
)
from .type_defs import (
    BatchPutMessageResponseTypeDef,
    ChannelMessagesTypeDef,
    ChannelStorageTypeDef,
    CreateChannelResponseTypeDef,
    CreateDatasetContentResponseTypeDef,
    CreateDatasetResponseTypeDef,
    CreateDatastoreResponseTypeDef,
    CreatePipelineResponseTypeDef,
    DatasetActionTypeDef,
    DatasetContentDeliveryRuleTypeDef,
    DatasetTriggerTypeDef,
    DatastoreStorageTypeDef,
    DescribeChannelResponseTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeDatastoreResponseTypeDef,
    DescribeLoggingOptionsResponseTypeDef,
    DescribePipelineResponseTypeDef,
    FileFormatConfigurationTypeDef,
    GetDatasetContentResponseTypeDef,
    LateDataRuleTypeDef,
    ListChannelsResponseTypeDef,
    ListDatasetContentsResponseTypeDef,
    ListDatasetsResponseTypeDef,
    ListDatastoresResponseTypeDef,
    ListPipelinesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    LoggingOptionsTypeDef,
    MessageTypeDef,
    PipelineActivityTypeDef,
    RetentionPeriodTypeDef,
    RunPipelineActivityResponseTypeDef,
    SampleChannelDataResponseTypeDef,
    StartPipelineReprocessingResponseTypeDef,
    TagTypeDef,
    VersioningConfigurationTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("IoTAnalyticsClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class IoTAnalyticsClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def batch_put_message(
        self, channelName: str, messages: List[MessageTypeDef]
    ) -> BatchPutMessageResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.batch_put_message)
        [Show boto3-stubs documentation](./client.md#batch_put_message)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can_paginate)
        """

    def cancel_pipeline_reprocessing(
        self, pipelineName: str, reprocessingId: str
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.cancel_pipeline_reprocessing)
        [Show boto3-stubs documentation](./client.md#cancel_pipeline_reprocessing)
        """

    def create_channel(
        self,
        channelName: str,
        channelStorage: "ChannelStorageTypeDef" = None,
        retentionPeriod: "RetentionPeriodTypeDef" = None,
        tags: List["TagTypeDef"] = None,
    ) -> CreateChannelResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.create_channel)
        [Show boto3-stubs documentation](./client.md#create_channel)
        """

    def create_dataset(
        self,
        datasetName: str,
        actions: List["DatasetActionTypeDef"],
        triggers: List["DatasetTriggerTypeDef"] = None,
        contentDeliveryRules: List["DatasetContentDeliveryRuleTypeDef"] = None,
        retentionPeriod: "RetentionPeriodTypeDef" = None,
        versioningConfiguration: "VersioningConfigurationTypeDef" = None,
        tags: List["TagTypeDef"] = None,
        lateDataRules: List["LateDataRuleTypeDef"] = None,
    ) -> CreateDatasetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.create_dataset)
        [Show boto3-stubs documentation](./client.md#create_dataset)
        """

    def create_dataset_content(
        self, datasetName: str, versionId: str = None
    ) -> CreateDatasetContentResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.create_dataset_content)
        [Show boto3-stubs documentation](./client.md#create_dataset_content)
        """

    def create_datastore(
        self,
        datastoreName: str,
        datastoreStorage: "DatastoreStorageTypeDef" = None,
        retentionPeriod: "RetentionPeriodTypeDef" = None,
        tags: List["TagTypeDef"] = None,
        fileFormatConfiguration: "FileFormatConfigurationTypeDef" = None,
    ) -> CreateDatastoreResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.create_datastore)
        [Show boto3-stubs documentation](./client.md#create_datastore)
        """

    def create_pipeline(
        self,
        pipelineName: str,
        pipelineActivities: List["PipelineActivityTypeDef"],
        tags: List["TagTypeDef"] = None,
    ) -> CreatePipelineResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.create_pipeline)
        [Show boto3-stubs documentation](./client.md#create_pipeline)
        """

    def delete_channel(self, channelName: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.delete_channel)
        [Show boto3-stubs documentation](./client.md#delete_channel)
        """

    def delete_dataset(self, datasetName: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.delete_dataset)
        [Show boto3-stubs documentation](./client.md#delete_dataset)
        """

    def delete_dataset_content(self, datasetName: str, versionId: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.delete_dataset_content)
        [Show boto3-stubs documentation](./client.md#delete_dataset_content)
        """

    def delete_datastore(self, datastoreName: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.delete_datastore)
        [Show boto3-stubs documentation](./client.md#delete_datastore)
        """

    def delete_pipeline(self, pipelineName: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.delete_pipeline)
        [Show boto3-stubs documentation](./client.md#delete_pipeline)
        """

    def describe_channel(
        self, channelName: str, includeStatistics: bool = None
    ) -> DescribeChannelResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.describe_channel)
        [Show boto3-stubs documentation](./client.md#describe_channel)
        """

    def describe_dataset(self, datasetName: str) -> DescribeDatasetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.describe_dataset)
        [Show boto3-stubs documentation](./client.md#describe_dataset)
        """

    def describe_datastore(
        self, datastoreName: str, includeStatistics: bool = None
    ) -> DescribeDatastoreResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.describe_datastore)
        [Show boto3-stubs documentation](./client.md#describe_datastore)
        """

    def describe_logging_options(self) -> DescribeLoggingOptionsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.describe_logging_options)
        [Show boto3-stubs documentation](./client.md#describe_logging_options)
        """

    def describe_pipeline(self, pipelineName: str) -> DescribePipelineResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.describe_pipeline)
        [Show boto3-stubs documentation](./client.md#describe_pipeline)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate_presigned_url)
        """

    def get_dataset_content(
        self, datasetName: str, versionId: str = None
    ) -> GetDatasetContentResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.get_dataset_content)
        [Show boto3-stubs documentation](./client.md#get_dataset_content)
        """

    def list_channels(
        self, nextToken: str = None, maxResults: int = None
    ) -> ListChannelsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.list_channels)
        [Show boto3-stubs documentation](./client.md#list_channels)
        """

    def list_dataset_contents(
        self,
        datasetName: str,
        nextToken: str = None,
        maxResults: int = None,
        scheduledOnOrAfter: datetime = None,
        scheduledBefore: datetime = None,
    ) -> ListDatasetContentsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.list_dataset_contents)
        [Show boto3-stubs documentation](./client.md#list_dataset_contents)
        """

    def list_datasets(
        self, nextToken: str = None, maxResults: int = None
    ) -> ListDatasetsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.list_datasets)
        [Show boto3-stubs documentation](./client.md#list_datasets)
        """

    def list_datastores(
        self, nextToken: str = None, maxResults: int = None
    ) -> ListDatastoresResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.list_datastores)
        [Show boto3-stubs documentation](./client.md#list_datastores)
        """

    def list_pipelines(
        self, nextToken: str = None, maxResults: int = None
    ) -> ListPipelinesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.list_pipelines)
        [Show boto3-stubs documentation](./client.md#list_pipelines)
        """

    def list_tags_for_resource(self, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#list_tags_for_resource)
        """

    def put_logging_options(self, loggingOptions: "LoggingOptionsTypeDef") -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.put_logging_options)
        [Show boto3-stubs documentation](./client.md#put_logging_options)
        """

    def run_pipeline_activity(
        self, pipelineActivity: "PipelineActivityTypeDef", payloads: List[Union[bytes, IO[bytes]]]
    ) -> RunPipelineActivityResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.run_pipeline_activity)
        [Show boto3-stubs documentation](./client.md#run_pipeline_activity)
        """

    def sample_channel_data(
        self,
        channelName: str,
        maxMessages: int = None,
        startTime: datetime = None,
        endTime: datetime = None,
    ) -> SampleChannelDataResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.sample_channel_data)
        [Show boto3-stubs documentation](./client.md#sample_channel_data)
        """

    def start_pipeline_reprocessing(
        self,
        pipelineName: str,
        startTime: datetime = None,
        endTime: datetime = None,
        channelMessages: ChannelMessagesTypeDef = None,
    ) -> StartPipelineReprocessingResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.start_pipeline_reprocessing)
        [Show boto3-stubs documentation](./client.md#start_pipeline_reprocessing)
        """

    def tag_resource(self, resourceArn: str, tags: List["TagTypeDef"]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag_resource)
        """

    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag_resource)
        """

    def update_channel(
        self,
        channelName: str,
        channelStorage: "ChannelStorageTypeDef" = None,
        retentionPeriod: "RetentionPeriodTypeDef" = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.update_channel)
        [Show boto3-stubs documentation](./client.md#update_channel)
        """

    def update_dataset(
        self,
        datasetName: str,
        actions: List["DatasetActionTypeDef"],
        triggers: List["DatasetTriggerTypeDef"] = None,
        contentDeliveryRules: List["DatasetContentDeliveryRuleTypeDef"] = None,
        retentionPeriod: "RetentionPeriodTypeDef" = None,
        versioningConfiguration: "VersioningConfigurationTypeDef" = None,
        lateDataRules: List["LateDataRuleTypeDef"] = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.update_dataset)
        [Show boto3-stubs documentation](./client.md#update_dataset)
        """

    def update_datastore(
        self,
        datastoreName: str,
        retentionPeriod: "RetentionPeriodTypeDef" = None,
        datastoreStorage: "DatastoreStorageTypeDef" = None,
        fileFormatConfiguration: "FileFormatConfigurationTypeDef" = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.update_datastore)
        [Show boto3-stubs documentation](./client.md#update_datastore)
        """

    def update_pipeline(
        self, pipelineName: str, pipelineActivities: List["PipelineActivityTypeDef"]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Client.update_pipeline)
        [Show boto3-stubs documentation](./client.md#update_pipeline)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Paginator.ListChannels)[Show boto3-stubs documentation](./paginators.md#listchannelspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataset_contents"]
    ) -> ListDatasetContentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Paginator.ListDatasetContents)[Show boto3-stubs documentation](./paginators.md#listdatasetcontentspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_datasets"]) -> ListDatasetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Paginator.ListDatasets)[Show boto3-stubs documentation](./paginators.md#listdatasetspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_datastores"]) -> ListDatastoresPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Paginator.ListDatastores)[Show boto3-stubs documentation](./paginators.md#listdatastorespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_pipelines"]) -> ListPipelinesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/iotanalytics.html#IoTAnalytics.Paginator.ListPipelines)[Show boto3-stubs documentation](./paginators.md#listpipelinespaginator)
        """
