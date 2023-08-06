"""
Type annotations for eks service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_eks import EKSClient
    from mypy_boto3_eks.paginator import (
        DescribeAddonVersionsPaginator,
        ListAddonsPaginator,
        ListClustersPaginator,
        ListFargateProfilesPaginator,
        ListIdentityProviderConfigsPaginator,
        ListNodegroupsPaginator,
        ListUpdatesPaginator,
    )

    client: EKSClient = boto3.client("eks")

    describe_addon_versions_paginator: DescribeAddonVersionsPaginator = client.get_paginator("describe_addon_versions")
    list_addons_paginator: ListAddonsPaginator = client.get_paginator("list_addons")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_fargate_profiles_paginator: ListFargateProfilesPaginator = client.get_paginator("list_fargate_profiles")
    list_identity_provider_configs_paginator: ListIdentityProviderConfigsPaginator = client.get_paginator("list_identity_provider_configs")
    list_nodegroups_paginator: ListNodegroupsPaginator = client.get_paginator("list_nodegroups")
    list_updates_paginator: ListUpdatesPaginator = client.get_paginator("list_updates")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    DescribeAddonVersionsResponseTypeDef,
    ListAddonsResponseTypeDef,
    ListClustersResponseTypeDef,
    ListFargateProfilesResponseTypeDef,
    ListIdentityProviderConfigsResponseTypeDef,
    ListNodegroupsResponseTypeDef,
    ListUpdatesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeAddonVersionsPaginator",
    "ListAddonsPaginator",
    "ListClustersPaginator",
    "ListFargateProfilesPaginator",
    "ListIdentityProviderConfigsPaginator",
    "ListNodegroupsPaginator",
    "ListUpdatesPaginator",
)


class DescribeAddonVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.DescribeAddonVersions)[Show boto3-stubs documentation](./paginators.md#describeaddonversionspaginator)
    """

    def paginate(
        self,
        kubernetesVersion: str = None,
        addonName: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeAddonVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.DescribeAddonVersions.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeaddonversionspaginator)
        """


class ListAddonsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.ListAddons)[Show boto3-stubs documentation](./paginators.md#listaddonspaginator)
    """

    def paginate(
        self, clusterName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListAddonsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.ListAddons.paginate)
        [Show boto3-stubs documentation](./paginators.md#listaddonspaginator)
        """


class ListClustersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.ListClusters)[Show boto3-stubs documentation](./paginators.md#listclusterspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.ListClusters.paginate)
        [Show boto3-stubs documentation](./paginators.md#listclusterspaginator)
        """


class ListFargateProfilesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.ListFargateProfiles)[Show boto3-stubs documentation](./paginators.md#listfargateprofilespaginator)
    """

    def paginate(
        self, clusterName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListFargateProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.ListFargateProfiles.paginate)
        [Show boto3-stubs documentation](./paginators.md#listfargateprofilespaginator)
        """


class ListIdentityProviderConfigsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.ListIdentityProviderConfigs)[Show boto3-stubs documentation](./paginators.md#listidentityproviderconfigspaginator)
    """

    def paginate(
        self, clusterName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListIdentityProviderConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.ListIdentityProviderConfigs.paginate)
        [Show boto3-stubs documentation](./paginators.md#listidentityproviderconfigspaginator)
        """


class ListNodegroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.ListNodegroups)[Show boto3-stubs documentation](./paginators.md#listnodegroupspaginator)
    """

    def paginate(
        self, clusterName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListNodegroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.ListNodegroups.paginate)
        [Show boto3-stubs documentation](./paginators.md#listnodegroupspaginator)
        """


class ListUpdatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.ListUpdates)[Show boto3-stubs documentation](./paginators.md#listupdatespaginator)
    """

    def paginate(
        self,
        name: str,
        nodegroupName: str = None,
        addonName: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Paginator.ListUpdates.paginate)
        [Show boto3-stubs documentation](./paginators.md#listupdatespaginator)
        """
