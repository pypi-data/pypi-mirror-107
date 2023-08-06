"""
Type annotations for sso service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_sso import SSOClient
    from mypy_boto3_sso.paginator import (
        ListAccountRolesPaginator,
        ListAccountsPaginator,
    )

    client: SSOClient = boto3.client("sso")

    list_account_roles_paginator: ListAccountRolesPaginator = client.get_paginator("list_account_roles")
    list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListAccountRolesResponseTypeDef,
    ListAccountsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListAccountRolesPaginator", "ListAccountsPaginator")


class ListAccountRolesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/sso.html#SSO.Paginator.ListAccountRoles)[Show boto3-stubs documentation](./paginators.md#listaccountrolespaginator)
    """

    def paginate(
        self, accessToken: str, accountId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListAccountRolesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/sso.html#SSO.Paginator.ListAccountRoles.paginate)
        [Show boto3-stubs documentation](./paginators.md#listaccountrolespaginator)
        """


class ListAccountsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/sso.html#SSO.Paginator.ListAccounts)[Show boto3-stubs documentation](./paginators.md#listaccountspaginator)
    """

    def paginate(
        self, accessToken: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/sso.html#SSO.Paginator.ListAccounts.paginate)
        [Show boto3-stubs documentation](./paginators.md#listaccountspaginator)
        """
