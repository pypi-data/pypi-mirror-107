"""
Type annotations for databrew service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_databrew import GlueDataBrewClient
    from mypy_boto3_databrew.paginator import (
        ListDatasetsPaginator,
        ListJobRunsPaginator,
        ListJobsPaginator,
        ListProjectsPaginator,
        ListRecipeVersionsPaginator,
        ListRecipesPaginator,
        ListSchedulesPaginator,
    )

    client: GlueDataBrewClient = boto3.client("databrew")

    list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
    list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    list_recipe_versions_paginator: ListRecipeVersionsPaginator = client.get_paginator("list_recipe_versions")
    list_recipes_paginator: ListRecipesPaginator = client.get_paginator("list_recipes")
    list_schedules_paginator: ListSchedulesPaginator = client.get_paginator("list_schedules")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListDatasetsResponseTypeDef,
    ListJobRunsResponseTypeDef,
    ListJobsResponseTypeDef,
    ListProjectsResponseTypeDef,
    ListRecipesResponseTypeDef,
    ListRecipeVersionsResponseTypeDef,
    ListSchedulesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListDatasetsPaginator",
    "ListJobRunsPaginator",
    "ListJobsPaginator",
    "ListProjectsPaginator",
    "ListRecipeVersionsPaginator",
    "ListRecipesPaginator",
    "ListSchedulesPaginator",
)


class ListDatasetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListDatasets)[Show boto3-stubs documentation](./paginators.md#listdatasetspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListDatasets.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdatasetspaginator)
        """


class ListJobRunsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListJobRuns)[Show boto3-stubs documentation](./paginators.md#listjobrunspaginator)
    """

    def paginate(
        self, Name: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListJobRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListJobRuns.paginate)
        [Show boto3-stubs documentation](./paginators.md#listjobrunspaginator)
        """


class ListJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListJobs)[Show boto3-stubs documentation](./paginators.md#listjobspaginator)
    """

    def paginate(
        self,
        DatasetName: str = None,
        ProjectName: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListJobs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listjobspaginator)
        """


class ListProjectsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListProjects)[Show boto3-stubs documentation](./paginators.md#listprojectspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListProjects.paginate)
        [Show boto3-stubs documentation](./paginators.md#listprojectspaginator)
        """


class ListRecipeVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListRecipeVersions)[Show boto3-stubs documentation](./paginators.md#listrecipeversionspaginator)
    """

    def paginate(
        self, Name: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListRecipeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListRecipeVersions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listrecipeversionspaginator)
        """


class ListRecipesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListRecipes)[Show boto3-stubs documentation](./paginators.md#listrecipespaginator)
    """

    def paginate(
        self, RecipeVersion: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListRecipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListRecipes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listrecipespaginator)
        """


class ListSchedulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListSchedules)[Show boto3-stubs documentation](./paginators.md#listschedulespaginator)
    """

    def paginate(
        self, JobName: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/databrew.html#GlueDataBrew.Paginator.ListSchedules.paginate)
        [Show boto3-stubs documentation](./paginators.md#listschedulespaginator)
        """
