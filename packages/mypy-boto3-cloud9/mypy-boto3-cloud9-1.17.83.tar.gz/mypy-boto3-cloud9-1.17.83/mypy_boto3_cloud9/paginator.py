"""
Type annotations for cloud9 service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_cloud9 import Cloud9Client
    from mypy_boto3_cloud9.paginator import (
        DescribeEnvironmentMembershipsPaginator,
        ListEnvironmentsPaginator,
    )

    client: Cloud9Client = boto3.client("cloud9")

    describe_environment_memberships_paginator: DescribeEnvironmentMembershipsPaginator = client.get_paginator("describe_environment_memberships")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .literals import PermissionsType
from .type_defs import (
    DescribeEnvironmentMembershipsResultTypeDef,
    ListEnvironmentsResultTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("DescribeEnvironmentMembershipsPaginator", "ListEnvironmentsPaginator")


class DescribeEnvironmentMembershipsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloud9.html#Cloud9.Paginator.DescribeEnvironmentMemberships)[Show boto3-stubs documentation](./paginators.md#describeenvironmentmembershipspaginator)
    """

    def paginate(
        self,
        userArn: str = None,
        environmentId: str = None,
        permissions: List[PermissionsType] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeEnvironmentMembershipsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloud9.html#Cloud9.Paginator.DescribeEnvironmentMemberships.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeenvironmentmembershipspaginator)
        """


class ListEnvironmentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloud9.html#Cloud9.Paginator.ListEnvironments)[Show boto3-stubs documentation](./paginators.md#listenvironmentspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListEnvironmentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloud9.html#Cloud9.Paginator.ListEnvironments.paginate)
        [Show boto3-stubs documentation](./paginators.md#listenvironmentspaginator)
        """
