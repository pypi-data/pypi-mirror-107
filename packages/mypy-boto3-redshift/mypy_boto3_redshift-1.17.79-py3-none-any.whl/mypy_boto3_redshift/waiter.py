"""
Type annotations for redshift service client waiters.

[Open documentation](./waiters.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_redshift import RedshiftClient
    from mypy_boto3_redshift.waiter import (
        ClusterAvailableWaiter,
        ClusterDeletedWaiter,
        ClusterRestoredWaiter,
        SnapshotAvailableWaiter,
    )

    client: RedshiftClient = boto3.client("redshift")

    cluster_available_waiter: ClusterAvailableWaiter = client.get_waiter("cluster_available")
    cluster_deleted_waiter: ClusterDeletedWaiter = client.get_waiter("cluster_deleted")
    cluster_restored_waiter: ClusterRestoredWaiter = client.get_waiter("cluster_restored")
    snapshot_available_waiter: SnapshotAvailableWaiter = client.get_waiter("snapshot_available")
    ```
"""
from datetime import datetime
from typing import List

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import SnapshotSortingEntityTypeDef, WaiterConfigTypeDef

__all__ = (
    "ClusterAvailableWaiter",
    "ClusterDeletedWaiter",
    "ClusterRestoredWaiter",
    "SnapshotAvailableWaiter",
)


class ClusterAvailableWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift.html#Redshift.Waiter.cluster_available)[Show boto3-stubs documentation](./waiters.md#clusteravailablewaiter)
    """

    def wait(
        self,
        ClusterIdentifier: str = None,
        MaxRecords: int = None,
        Marker: str = None,
        TagKeys: List[str] = None,
        TagValues: List[str] = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift.html#Redshift.Waiter.ClusterAvailableWaiter)
        [Show boto3-stubs documentation](./waiters.md#clusteravailable)
        """


class ClusterDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift.html#Redshift.Waiter.cluster_deleted)[Show boto3-stubs documentation](./waiters.md#clusterdeletedwaiter)
    """

    def wait(
        self,
        ClusterIdentifier: str = None,
        MaxRecords: int = None,
        Marker: str = None,
        TagKeys: List[str] = None,
        TagValues: List[str] = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift.html#Redshift.Waiter.ClusterDeletedWaiter)
        [Show boto3-stubs documentation](./waiters.md#clusterdeleted)
        """


class ClusterRestoredWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift.html#Redshift.Waiter.cluster_restored)[Show boto3-stubs documentation](./waiters.md#clusterrestoredwaiter)
    """

    def wait(
        self,
        ClusterIdentifier: str = None,
        MaxRecords: int = None,
        Marker: str = None,
        TagKeys: List[str] = None,
        TagValues: List[str] = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift.html#Redshift.Waiter.ClusterRestoredWaiter)
        [Show boto3-stubs documentation](./waiters.md#clusterrestored)
        """


class SnapshotAvailableWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift.html#Redshift.Waiter.snapshot_available)[Show boto3-stubs documentation](./waiters.md#snapshotavailablewaiter)
    """

    def wait(
        self,
        ClusterIdentifier: str = None,
        SnapshotIdentifier: str = None,
        SnapshotType: str = None,
        StartTime: datetime = None,
        EndTime: datetime = None,
        MaxRecords: int = None,
        Marker: str = None,
        OwnerAccount: str = None,
        TagKeys: List[str] = None,
        TagValues: List[str] = None,
        ClusterExists: bool = None,
        SortingEntities: List[SnapshotSortingEntityTypeDef] = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/redshift.html#Redshift.Waiter.SnapshotAvailableWaiter)
        [Show boto3-stubs documentation](./waiters.md#snapshotavailable)
        """
