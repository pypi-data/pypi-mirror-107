"""
Type annotations for lookoutvision service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_lookoutvision import LookoutforVisionClient

    client: LookoutforVisionClient = boto3.client("lookoutvision")
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Type, Union, overload

from botocore.client import ClientMeta

from .paginator import ListDatasetEntriesPaginator, ListModelsPaginator, ListProjectsPaginator
from .type_defs import (
    CreateDatasetResponseTypeDef,
    CreateModelResponseTypeDef,
    CreateProjectResponseTypeDef,
    DatasetSourceTypeDef,
    DeleteModelResponseTypeDef,
    DeleteProjectResponseTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeModelResponseTypeDef,
    DescribeProjectResponseTypeDef,
    DetectAnomaliesResponseTypeDef,
    ListDatasetEntriesResponseTypeDef,
    ListModelsResponseTypeDef,
    ListProjectsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    OutputConfigTypeDef,
    StartModelResponseTypeDef,
    StopModelResponseTypeDef,
    TagTypeDef,
    UpdateDatasetEntriesResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("LookoutforVisionClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LookoutforVisionClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can_paginate)
        """

    def create_dataset(
        self,
        ProjectName: str,
        DatasetType: str,
        DatasetSource: DatasetSourceTypeDef = None,
        ClientToken: str = None,
    ) -> CreateDatasetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.create_dataset)
        [Show boto3-stubs documentation](./client.md#create_dataset)
        """

    def create_model(
        self,
        ProjectName: str,
        OutputConfig: "OutputConfigTypeDef",
        Description: str = None,
        ClientToken: str = None,
        KmsKeyId: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateModelResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.create_model)
        [Show boto3-stubs documentation](./client.md#create_model)
        """

    def create_project(
        self, ProjectName: str, ClientToken: str = None
    ) -> CreateProjectResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.create_project)
        [Show boto3-stubs documentation](./client.md#create_project)
        """

    def delete_dataset(
        self, ProjectName: str, DatasetType: str, ClientToken: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.delete_dataset)
        [Show boto3-stubs documentation](./client.md#delete_dataset)
        """

    def delete_model(
        self, ProjectName: str, ModelVersion: str, ClientToken: str = None
    ) -> DeleteModelResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.delete_model)
        [Show boto3-stubs documentation](./client.md#delete_model)
        """

    def delete_project(
        self, ProjectName: str, ClientToken: str = None
    ) -> DeleteProjectResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.delete_project)
        [Show boto3-stubs documentation](./client.md#delete_project)
        """

    def describe_dataset(
        self, ProjectName: str, DatasetType: str
    ) -> DescribeDatasetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.describe_dataset)
        [Show boto3-stubs documentation](./client.md#describe_dataset)
        """

    def describe_model(self, ProjectName: str, ModelVersion: str) -> DescribeModelResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.describe_model)
        [Show boto3-stubs documentation](./client.md#describe_model)
        """

    def describe_project(self, ProjectName: str) -> DescribeProjectResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.describe_project)
        [Show boto3-stubs documentation](./client.md#describe_project)
        """

    def detect_anomalies(
        self, ProjectName: str, ModelVersion: str, Body: Union[bytes, IO[bytes]], ContentType: str
    ) -> DetectAnomaliesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.detect_anomalies)
        [Show boto3-stubs documentation](./client.md#detect_anomalies)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate_presigned_url)
        """

    def list_dataset_entries(
        self,
        ProjectName: str,
        DatasetType: str,
        Labeled: bool = None,
        AnomalyClass: str = None,
        BeforeCreationDate: datetime = None,
        AfterCreationDate: datetime = None,
        NextToken: str = None,
        MaxResults: int = None,
        SourceRefContains: str = None,
    ) -> ListDatasetEntriesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.list_dataset_entries)
        [Show boto3-stubs documentation](./client.md#list_dataset_entries)
        """

    def list_models(
        self, ProjectName: str, NextToken: str = None, MaxResults: int = None
    ) -> ListModelsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.list_models)
        [Show boto3-stubs documentation](./client.md#list_models)
        """

    def list_projects(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListProjectsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.list_projects)
        [Show boto3-stubs documentation](./client.md#list_projects)
        """

    def list_tags_for_resource(self, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#list_tags_for_resource)
        """

    def start_model(
        self, ProjectName: str, ModelVersion: str, MinInferenceUnits: int, ClientToken: str = None
    ) -> StartModelResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.start_model)
        [Show boto3-stubs documentation](./client.md#start_model)
        """

    def stop_model(
        self, ProjectName: str, ModelVersion: str, ClientToken: str = None
    ) -> StopModelResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.stop_model)
        [Show boto3-stubs documentation](./client.md#stop_model)
        """

    def tag_resource(self, ResourceArn: str, Tags: List["TagTypeDef"]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag_resource)
        """

    def untag_resource(self, ResourceArn: str, TagKeys: List[str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag_resource)
        """

    def update_dataset_entries(
        self,
        ProjectName: str,
        DatasetType: str,
        Changes: Union[bytes, IO[bytes]],
        ClientToken: str = None,
    ) -> UpdateDatasetEntriesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Client.update_dataset_entries)
        [Show boto3-stubs documentation](./client.md#update_dataset_entries)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataset_entries"]
    ) -> ListDatasetEntriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListDatasetEntries)[Show boto3-stubs documentation](./paginators.md#listdatasetentriespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_models"]) -> ListModelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListModels)[Show boto3-stubs documentation](./paginators.md#listmodelspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListProjects)[Show boto3-stubs documentation](./paginators.md#listprojectspaginator)
        """
