"""
Type annotations for resource-groups service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_resource_groups import ResourceGroupsClient
    from mypy_boto3_resource_groups.paginator import (
        ListGroupResourcesPaginator,
        ListGroupsPaginator,
        SearchResourcesPaginator,
    )

    client: ResourceGroupsClient = boto3.client("resource-groups")

    list_group_resources_paginator: ListGroupResourcesPaginator = client.get_paginator("list_group_resources")
    list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
    search_resources_paginator: SearchResourcesPaginator = client.get_paginator("search_resources")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    GroupFilterTypeDef,
    ListGroupResourcesOutputTypeDef,
    ListGroupsOutputTypeDef,
    PaginatorConfigTypeDef,
    ResourceFilterTypeDef,
    ResourceQueryTypeDef,
    SearchResourcesOutputTypeDef,
)

__all__ = ("ListGroupResourcesPaginator", "ListGroupsPaginator", "SearchResourcesPaginator")


class ListGroupResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroupResources)[Show boto3-stubs documentation](./paginators.md#listgroupresourcespaginator)
    """

    def paginate(
        self,
        GroupName: str = None,
        Group: str = None,
        Filters: List[ResourceFilterTypeDef] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListGroupResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroupResources.paginate)
        [Show boto3-stubs documentation](./paginators.md#listgroupresourcespaginator)
        """


class ListGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroups)[Show boto3-stubs documentation](./paginators.md#listgroupspaginator)
    """

    def paginate(
        self,
        Filters: List[GroupFilterTypeDef] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroups.paginate)
        [Show boto3-stubs documentation](./paginators.md#listgroupspaginator)
        """


class SearchResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/resource-groups.html#ResourceGroups.Paginator.SearchResources)[Show boto3-stubs documentation](./paginators.md#searchresourcespaginator)
    """

    def paginate(
        self, ResourceQuery: "ResourceQueryTypeDef", PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[SearchResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/resource-groups.html#ResourceGroups.Paginator.SearchResources.paginate)
        [Show boto3-stubs documentation](./paginators.md#searchresourcespaginator)
        """
