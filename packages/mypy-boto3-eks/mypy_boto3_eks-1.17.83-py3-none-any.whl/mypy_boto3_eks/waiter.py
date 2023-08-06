"""
Type annotations for eks service client waiters.

[Open documentation](./waiters.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_eks import EKSClient
    from mypy_boto3_eks.waiter import (
        AddonActiveWaiter,
        AddonDeletedWaiter,
        ClusterActiveWaiter,
        ClusterDeletedWaiter,
        NodegroupActiveWaiter,
        NodegroupDeletedWaiter,
    )

    client: EKSClient = boto3.client("eks")

    addon_active_waiter: AddonActiveWaiter = client.get_waiter("addon_active")
    addon_deleted_waiter: AddonDeletedWaiter = client.get_waiter("addon_deleted")
    cluster_active_waiter: ClusterActiveWaiter = client.get_waiter("cluster_active")
    cluster_deleted_waiter: ClusterDeletedWaiter = client.get_waiter("cluster_deleted")
    nodegroup_active_waiter: NodegroupActiveWaiter = client.get_waiter("nodegroup_active")
    nodegroup_deleted_waiter: NodegroupDeletedWaiter = client.get_waiter("nodegroup_deleted")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "AddonActiveWaiter",
    "AddonDeletedWaiter",
    "ClusterActiveWaiter",
    "ClusterDeletedWaiter",
    "NodegroupActiveWaiter",
    "NodegroupDeletedWaiter",
)


class AddonActiveWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Waiter.addon_active)[Show boto3-stubs documentation](./waiters.md#addonactivewaiter)
    """

    def wait(
        self, clusterName: str, addonName: str, WaiterConfig: WaiterConfigTypeDef = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Waiter.AddonActiveWaiter)
        [Show boto3-stubs documentation](./waiters.md#addonactive)
        """


class AddonDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Waiter.addon_deleted)[Show boto3-stubs documentation](./waiters.md#addondeletedwaiter)
    """

    def wait(
        self, clusterName: str, addonName: str, WaiterConfig: WaiterConfigTypeDef = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Waiter.AddonDeletedWaiter)
        [Show boto3-stubs documentation](./waiters.md#addondeleted)
        """


class ClusterActiveWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Waiter.cluster_active)[Show boto3-stubs documentation](./waiters.md#clusteractivewaiter)
    """

    def wait(self, name: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Waiter.ClusterActiveWaiter)
        [Show boto3-stubs documentation](./waiters.md#clusteractive)
        """


class ClusterDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Waiter.cluster_deleted)[Show boto3-stubs documentation](./waiters.md#clusterdeletedwaiter)
    """

    def wait(self, name: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Waiter.ClusterDeletedWaiter)
        [Show boto3-stubs documentation](./waiters.md#clusterdeleted)
        """


class NodegroupActiveWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Waiter.nodegroup_active)[Show boto3-stubs documentation](./waiters.md#nodegroupactivewaiter)
    """

    def wait(
        self, clusterName: str, nodegroupName: str, WaiterConfig: WaiterConfigTypeDef = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Waiter.NodegroupActiveWaiter)
        [Show boto3-stubs documentation](./waiters.md#nodegroupactive)
        """


class NodegroupDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Waiter.nodegroup_deleted)[Show boto3-stubs documentation](./waiters.md#nodegroupdeletedwaiter)
    """

    def wait(
        self, clusterName: str, nodegroupName: str, WaiterConfig: WaiterConfigTypeDef = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/eks.html#EKS.Waiter.NodegroupDeletedWaiter)
        [Show boto3-stubs documentation](./waiters.md#nodegroupdeleted)
        """
