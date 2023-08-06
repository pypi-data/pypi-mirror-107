"""
Type annotations for workmail service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_workmail import WorkMailClient
    from mypy_boto3_workmail.paginator import (
        ListAliasesPaginator,
        ListGroupMembersPaginator,
        ListGroupsPaginator,
        ListMailboxPermissionsPaginator,
        ListOrganizationsPaginator,
        ListResourceDelegatesPaginator,
        ListResourcesPaginator,
        ListUsersPaginator,
    )

    client: WorkMailClient = boto3.client("workmail")

    list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
    list_group_members_paginator: ListGroupMembersPaginator = client.get_paginator("list_group_members")
    list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
    list_mailbox_permissions_paginator: ListMailboxPermissionsPaginator = client.get_paginator("list_mailbox_permissions")
    list_organizations_paginator: ListOrganizationsPaginator = client.get_paginator("list_organizations")
    list_resource_delegates_paginator: ListResourceDelegatesPaginator = client.get_paginator("list_resource_delegates")
    list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListAliasesResponseTypeDef,
    ListGroupMembersResponseTypeDef,
    ListGroupsResponseTypeDef,
    ListMailboxPermissionsResponseTypeDef,
    ListOrganizationsResponseTypeDef,
    ListResourceDelegatesResponseTypeDef,
    ListResourcesResponseTypeDef,
    ListUsersResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListAliasesPaginator",
    "ListGroupMembersPaginator",
    "ListGroupsPaginator",
    "ListMailboxPermissionsPaginator",
    "ListOrganizationsPaginator",
    "ListResourceDelegatesPaginator",
    "ListResourcesPaginator",
    "ListUsersPaginator",
)


class ListAliasesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListAliases)[Show boto3-stubs documentation](./paginators.md#listaliasespaginator)
    """

    def paginate(
        self, OrganizationId: str, EntityId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListAliases.paginate)
        [Show boto3-stubs documentation](./paginators.md#listaliasespaginator)
        """


class ListGroupMembersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListGroupMembers)[Show boto3-stubs documentation](./paginators.md#listgroupmemberspaginator)
    """

    def paginate(
        self, OrganizationId: str, GroupId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListGroupMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListGroupMembers.paginate)
        [Show boto3-stubs documentation](./paginators.md#listgroupmemberspaginator)
        """


class ListGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListGroups)[Show boto3-stubs documentation](./paginators.md#listgroupspaginator)
    """

    def paginate(
        self, OrganizationId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListGroups.paginate)
        [Show boto3-stubs documentation](./paginators.md#listgroupspaginator)
        """


class ListMailboxPermissionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListMailboxPermissions)[Show boto3-stubs documentation](./paginators.md#listmailboxpermissionspaginator)
    """

    def paginate(
        self, OrganizationId: str, EntityId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListMailboxPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListMailboxPermissions.paginate)
        [Show boto3-stubs documentation](./paginators.md#listmailboxpermissionspaginator)
        """


class ListOrganizationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListOrganizations)[Show boto3-stubs documentation](./paginators.md#listorganizationspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListOrganizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListOrganizations.paginate)
        [Show boto3-stubs documentation](./paginators.md#listorganizationspaginator)
        """


class ListResourceDelegatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListResourceDelegates)[Show boto3-stubs documentation](./paginators.md#listresourcedelegatespaginator)
    """

    def paginate(
        self, OrganizationId: str, ResourceId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListResourceDelegatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListResourceDelegates.paginate)
        [Show boto3-stubs documentation](./paginators.md#listresourcedelegatespaginator)
        """


class ListResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListResources)[Show boto3-stubs documentation](./paginators.md#listresourcespaginator)
    """

    def paginate(
        self, OrganizationId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListResources.paginate)
        [Show boto3-stubs documentation](./paginators.md#listresourcespaginator)
        """


class ListUsersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListUsers)[Show boto3-stubs documentation](./paginators.md#listuserspaginator)
    """

    def paginate(
        self, OrganizationId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/workmail.html#WorkMail.Paginator.ListUsers.paginate)
        [Show boto3-stubs documentation](./paginators.md#listuserspaginator)
        """
