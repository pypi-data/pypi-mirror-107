"""
Type annotations for fms service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_fms import FMSClient
    from mypy_boto3_fms.paginator import (
        ListComplianceStatusPaginator,
        ListMemberAccountsPaginator,
        ListPoliciesPaginator,
    )

    client: FMSClient = boto3.client("fms")

    list_compliance_status_paginator: ListComplianceStatusPaginator = client.get_paginator("list_compliance_status")
    list_member_accounts_paginator: ListMemberAccountsPaginator = client.get_paginator("list_member_accounts")
    list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListComplianceStatusResponseTypeDef,
    ListMemberAccountsResponseTypeDef,
    ListPoliciesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListComplianceStatusPaginator", "ListMemberAccountsPaginator", "ListPoliciesPaginator")


class ListComplianceStatusPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/fms.html#FMS.Paginator.ListComplianceStatus)[Show boto3-stubs documentation](./paginators.md#listcompliancestatuspaginator)
    """

    def paginate(
        self, PolicyId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListComplianceStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/fms.html#FMS.Paginator.ListComplianceStatus.paginate)
        [Show boto3-stubs documentation](./paginators.md#listcompliancestatuspaginator)
        """


class ListMemberAccountsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/fms.html#FMS.Paginator.ListMemberAccounts)[Show boto3-stubs documentation](./paginators.md#listmemberaccountspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListMemberAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/fms.html#FMS.Paginator.ListMemberAccounts.paginate)
        [Show boto3-stubs documentation](./paginators.md#listmemberaccountspaginator)
        """


class ListPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/fms.html#FMS.Paginator.ListPolicies)[Show boto3-stubs documentation](./paginators.md#listpoliciespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/fms.html#FMS.Paginator.ListPolicies.paginate)
        [Show boto3-stubs documentation](./paginators.md#listpoliciespaginator)
        """
