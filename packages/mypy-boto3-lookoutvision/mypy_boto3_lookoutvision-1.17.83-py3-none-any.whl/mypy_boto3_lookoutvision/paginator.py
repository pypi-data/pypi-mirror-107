"""
Type annotations for lookoutvision service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_lookoutvision import LookoutforVisionClient
    from mypy_boto3_lookoutvision.paginator import (
        ListDatasetEntriesPaginator,
        ListModelsPaginator,
        ListProjectsPaginator,
    )

    client: LookoutforVisionClient = boto3.client("lookoutvision")

    list_dataset_entries_paginator: ListDatasetEntriesPaginator = client.get_paginator("list_dataset_entries")
    list_models_paginator: ListModelsPaginator = client.get_paginator("list_models")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```
"""
from datetime import datetime
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListDatasetEntriesResponseTypeDef,
    ListModelsResponseTypeDef,
    ListProjectsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListDatasetEntriesPaginator", "ListModelsPaginator", "ListProjectsPaginator")


class ListDatasetEntriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListDatasetEntries)[Show boto3-stubs documentation](./paginators.md#listdatasetentriespaginator)
    """

    def paginate(
        self,
        ProjectName: str,
        DatasetType: str,
        Labeled: bool = None,
        AnomalyClass: str = None,
        BeforeCreationDate: datetime = None,
        AfterCreationDate: datetime = None,
        SourceRefContains: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListDatasetEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListDatasetEntries.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdatasetentriespaginator)
        """


class ListModelsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListModels)[Show boto3-stubs documentation](./paginators.md#listmodelspaginator)
    """

    def paginate(
        self, ProjectName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListModels.paginate)
        [Show boto3-stubs documentation](./paginators.md#listmodelspaginator)
        """


class ListProjectsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListProjects)[Show boto3-stubs documentation](./paginators.md#listprojectspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListProjects.paginate)
        [Show boto3-stubs documentation](./paginators.md#listprojectspaginator)
        """
