"""
Type annotations for robomaker service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_robomaker import RoboMakerClient
    from mypy_boto3_robomaker.paginator import (
        ListDeploymentJobsPaginator,
        ListFleetsPaginator,
        ListRobotApplicationsPaginator,
        ListRobotsPaginator,
        ListSimulationApplicationsPaginator,
        ListSimulationJobBatchesPaginator,
        ListSimulationJobsPaginator,
        ListWorldExportJobsPaginator,
        ListWorldGenerationJobsPaginator,
        ListWorldTemplatesPaginator,
        ListWorldsPaginator,
    )

    client: RoboMakerClient = boto3.client("robomaker")

    list_deployment_jobs_paginator: ListDeploymentJobsPaginator = client.get_paginator("list_deployment_jobs")
    list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
    list_robot_applications_paginator: ListRobotApplicationsPaginator = client.get_paginator("list_robot_applications")
    list_robots_paginator: ListRobotsPaginator = client.get_paginator("list_robots")
    list_simulation_applications_paginator: ListSimulationApplicationsPaginator = client.get_paginator("list_simulation_applications")
    list_simulation_job_batches_paginator: ListSimulationJobBatchesPaginator = client.get_paginator("list_simulation_job_batches")
    list_simulation_jobs_paginator: ListSimulationJobsPaginator = client.get_paginator("list_simulation_jobs")
    list_world_export_jobs_paginator: ListWorldExportJobsPaginator = client.get_paginator("list_world_export_jobs")
    list_world_generation_jobs_paginator: ListWorldGenerationJobsPaginator = client.get_paginator("list_world_generation_jobs")
    list_world_templates_paginator: ListWorldTemplatesPaginator = client.get_paginator("list_world_templates")
    list_worlds_paginator: ListWorldsPaginator = client.get_paginator("list_worlds")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    FilterTypeDef,
    ListDeploymentJobsResponseTypeDef,
    ListFleetsResponseTypeDef,
    ListRobotApplicationsResponseTypeDef,
    ListRobotsResponseTypeDef,
    ListSimulationApplicationsResponseTypeDef,
    ListSimulationJobBatchesResponseTypeDef,
    ListSimulationJobsResponseTypeDef,
    ListWorldExportJobsResponseTypeDef,
    ListWorldGenerationJobsResponseTypeDef,
    ListWorldsResponseTypeDef,
    ListWorldTemplatesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListDeploymentJobsPaginator",
    "ListFleetsPaginator",
    "ListRobotApplicationsPaginator",
    "ListRobotsPaginator",
    "ListSimulationApplicationsPaginator",
    "ListSimulationJobBatchesPaginator",
    "ListSimulationJobsPaginator",
    "ListWorldExportJobsPaginator",
    "ListWorldGenerationJobsPaginator",
    "ListWorldTemplatesPaginator",
    "ListWorldsPaginator",
)


class ListDeploymentJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListDeploymentJobs)[Show boto3-stubs documentation](./paginators.md#listdeploymentjobspaginator)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListDeploymentJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListDeploymentJobs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdeploymentjobspaginator)
        """


class ListFleetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListFleets)[Show boto3-stubs documentation](./paginators.md#listfleetspaginator)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListFleets.paginate)
        [Show boto3-stubs documentation](./paginators.md#listfleetspaginator)
        """


class ListRobotApplicationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListRobotApplications)[Show boto3-stubs documentation](./paginators.md#listrobotapplicationspaginator)
    """

    def paginate(
        self,
        versionQualifier: str = None,
        filters: List[FilterTypeDef] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListRobotApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListRobotApplications.paginate)
        [Show boto3-stubs documentation](./paginators.md#listrobotapplicationspaginator)
        """


class ListRobotsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListRobots)[Show boto3-stubs documentation](./paginators.md#listrobotspaginator)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListRobotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListRobots.paginate)
        [Show boto3-stubs documentation](./paginators.md#listrobotspaginator)
        """


class ListSimulationApplicationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationApplications)[Show boto3-stubs documentation](./paginators.md#listsimulationapplicationspaginator)
    """

    def paginate(
        self,
        versionQualifier: str = None,
        filters: List[FilterTypeDef] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListSimulationApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationApplications.paginate)
        [Show boto3-stubs documentation](./paginators.md#listsimulationapplicationspaginator)
        """


class ListSimulationJobBatchesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationJobBatches)[Show boto3-stubs documentation](./paginators.md#listsimulationjobbatchespaginator)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSimulationJobBatchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationJobBatches.paginate)
        [Show boto3-stubs documentation](./paginators.md#listsimulationjobbatchespaginator)
        """


class ListSimulationJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationJobs)[Show boto3-stubs documentation](./paginators.md#listsimulationjobspaginator)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSimulationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationJobs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listsimulationjobspaginator)
        """


class ListWorldExportJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListWorldExportJobs)[Show boto3-stubs documentation](./paginators.md#listworldexportjobspaginator)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListWorldExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListWorldExportJobs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listworldexportjobspaginator)
        """


class ListWorldGenerationJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListWorldGenerationJobs)[Show boto3-stubs documentation](./paginators.md#listworldgenerationjobspaginator)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListWorldGenerationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListWorldGenerationJobs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listworldgenerationjobspaginator)
        """


class ListWorldTemplatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListWorldTemplates)[Show boto3-stubs documentation](./paginators.md#listworldtemplatespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListWorldTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListWorldTemplates.paginate)
        [Show boto3-stubs documentation](./paginators.md#listworldtemplatespaginator)
        """


class ListWorldsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListWorlds)[Show boto3-stubs documentation](./paginators.md#listworldspaginator)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListWorldsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/robomaker.html#RoboMaker.Paginator.ListWorlds.paginate)
        [Show boto3-stubs documentation](./paginators.md#listworldspaginator)
        """
