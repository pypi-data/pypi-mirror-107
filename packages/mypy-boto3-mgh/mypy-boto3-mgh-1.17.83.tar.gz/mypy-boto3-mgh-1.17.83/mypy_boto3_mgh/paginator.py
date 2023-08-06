"""
Type annotations for mgh service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_mgh import MigrationHubClient
    from mypy_boto3_mgh.paginator import (
        ListApplicationStatesPaginator,
        ListCreatedArtifactsPaginator,
        ListDiscoveredResourcesPaginator,
        ListMigrationTasksPaginator,
        ListProgressUpdateStreamsPaginator,
    )

    client: MigrationHubClient = boto3.client("mgh")

    list_application_states_paginator: ListApplicationStatesPaginator = client.get_paginator("list_application_states")
    list_created_artifacts_paginator: ListCreatedArtifactsPaginator = client.get_paginator("list_created_artifacts")
    list_discovered_resources_paginator: ListDiscoveredResourcesPaginator = client.get_paginator("list_discovered_resources")
    list_migration_tasks_paginator: ListMigrationTasksPaginator = client.get_paginator("list_migration_tasks")
    list_progress_update_streams_paginator: ListProgressUpdateStreamsPaginator = client.get_paginator("list_progress_update_streams")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListApplicationStatesResultTypeDef,
    ListCreatedArtifactsResultTypeDef,
    ListDiscoveredResourcesResultTypeDef,
    ListMigrationTasksResultTypeDef,
    ListProgressUpdateStreamsResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListApplicationStatesPaginator",
    "ListCreatedArtifactsPaginator",
    "ListDiscoveredResourcesPaginator",
    "ListMigrationTasksPaginator",
    "ListProgressUpdateStreamsPaginator",
)


class ListApplicationStatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/mgh.html#MigrationHub.Paginator.ListApplicationStates)[Show boto3-stubs documentation](./paginators.md#listapplicationstatespaginator)
    """

    def paginate(
        self, ApplicationIds: List[str] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListApplicationStatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/mgh.html#MigrationHub.Paginator.ListApplicationStates.paginate)
        [Show boto3-stubs documentation](./paginators.md#listapplicationstatespaginator)
        """


class ListCreatedArtifactsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/mgh.html#MigrationHub.Paginator.ListCreatedArtifacts)[Show boto3-stubs documentation](./paginators.md#listcreatedartifactspaginator)
    """

    def paginate(
        self,
        ProgressUpdateStream: str,
        MigrationTaskName: str,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListCreatedArtifactsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/mgh.html#MigrationHub.Paginator.ListCreatedArtifacts.paginate)
        [Show boto3-stubs documentation](./paginators.md#listcreatedartifactspaginator)
        """


class ListDiscoveredResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/mgh.html#MigrationHub.Paginator.ListDiscoveredResources)[Show boto3-stubs documentation](./paginators.md#listdiscoveredresourcespaginator)
    """

    def paginate(
        self,
        ProgressUpdateStream: str,
        MigrationTaskName: str,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListDiscoveredResourcesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/mgh.html#MigrationHub.Paginator.ListDiscoveredResources.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdiscoveredresourcespaginator)
        """


class ListMigrationTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/mgh.html#MigrationHub.Paginator.ListMigrationTasks)[Show boto3-stubs documentation](./paginators.md#listmigrationtaskspaginator)
    """

    def paginate(
        self, ResourceName: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListMigrationTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/mgh.html#MigrationHub.Paginator.ListMigrationTasks.paginate)
        [Show boto3-stubs documentation](./paginators.md#listmigrationtaskspaginator)
        """


class ListProgressUpdateStreamsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/mgh.html#MigrationHub.Paginator.ListProgressUpdateStreams)[Show boto3-stubs documentation](./paginators.md#listprogressupdatestreamspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListProgressUpdateStreamsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/mgh.html#MigrationHub.Paginator.ListProgressUpdateStreams.paginate)
        [Show boto3-stubs documentation](./paginators.md#listprogressupdatestreamspaginator)
        """
