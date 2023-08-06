"""
Type annotations for dms service client waiters.

[Open documentation](./waiters.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_dms import DatabaseMigrationServiceClient
    from mypy_boto3_dms.waiter import (
        EndpointDeletedWaiter,
        ReplicationInstanceAvailableWaiter,
        ReplicationInstanceDeletedWaiter,
        ReplicationTaskDeletedWaiter,
        ReplicationTaskReadyWaiter,
        ReplicationTaskRunningWaiter,
        ReplicationTaskStoppedWaiter,
        TestConnectionSucceedsWaiter,
    )

    client: DatabaseMigrationServiceClient = boto3.client("dms")

    endpoint_deleted_waiter: EndpointDeletedWaiter = client.get_waiter("endpoint_deleted")
    replication_instance_available_waiter: ReplicationInstanceAvailableWaiter = client.get_waiter("replication_instance_available")
    replication_instance_deleted_waiter: ReplicationInstanceDeletedWaiter = client.get_waiter("replication_instance_deleted")
    replication_task_deleted_waiter: ReplicationTaskDeletedWaiter = client.get_waiter("replication_task_deleted")
    replication_task_ready_waiter: ReplicationTaskReadyWaiter = client.get_waiter("replication_task_ready")
    replication_task_running_waiter: ReplicationTaskRunningWaiter = client.get_waiter("replication_task_running")
    replication_task_stopped_waiter: ReplicationTaskStoppedWaiter = client.get_waiter("replication_task_stopped")
    test_connection_succeeds_waiter: TestConnectionSucceedsWaiter = client.get_waiter("test_connection_succeeds")
    ```
"""
from typing import List

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import FilterTypeDef, WaiterConfigTypeDef

__all__ = (
    "EndpointDeletedWaiter",
    "ReplicationInstanceAvailableWaiter",
    "ReplicationInstanceDeletedWaiter",
    "ReplicationTaskDeletedWaiter",
    "ReplicationTaskReadyWaiter",
    "ReplicationTaskRunningWaiter",
    "ReplicationTaskStoppedWaiter",
    "TestConnectionSucceedsWaiter",
)


class EndpointDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.endpoint_deleted)[Show boto3-stubs documentation](./waiters.md#endpointdeletedwaiter)
    """

    def wait(
        self,
        Filters: List[FilterTypeDef] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.EndpointDeletedWaiter)
        [Show boto3-stubs documentation](./waiters.md#endpointdeleted)
        """


class ReplicationInstanceAvailableWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.replication_instance_available)[Show boto3-stubs documentation](./waiters.md#replicationinstanceavailablewaiter)
    """

    def wait(
        self,
        Filters: List[FilterTypeDef] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationInstanceAvailableWaiter)
        [Show boto3-stubs documentation](./waiters.md#replicationinstanceavailable)
        """


class ReplicationInstanceDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.replication_instance_deleted)[Show boto3-stubs documentation](./waiters.md#replicationinstancedeletedwaiter)
    """

    def wait(
        self,
        Filters: List[FilterTypeDef] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationInstanceDeletedWaiter)
        [Show boto3-stubs documentation](./waiters.md#replicationinstancedeleted)
        """


class ReplicationTaskDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.replication_task_deleted)[Show boto3-stubs documentation](./waiters.md#replicationtaskdeletedwaiter)
    """

    def wait(
        self,
        Filters: List[FilterTypeDef] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WithoutSettings: bool = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationTaskDeletedWaiter)
        [Show boto3-stubs documentation](./waiters.md#replicationtaskdeleted)
        """


class ReplicationTaskReadyWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.replication_task_ready)[Show boto3-stubs documentation](./waiters.md#replicationtaskreadywaiter)
    """

    def wait(
        self,
        Filters: List[FilterTypeDef] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WithoutSettings: bool = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationTaskReadyWaiter)
        [Show boto3-stubs documentation](./waiters.md#replicationtaskready)
        """


class ReplicationTaskRunningWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.replication_task_running)[Show boto3-stubs documentation](./waiters.md#replicationtaskrunningwaiter)
    """

    def wait(
        self,
        Filters: List[FilterTypeDef] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WithoutSettings: bool = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationTaskRunningWaiter)
        [Show boto3-stubs documentation](./waiters.md#replicationtaskrunning)
        """


class ReplicationTaskStoppedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.replication_task_stopped)[Show boto3-stubs documentation](./waiters.md#replicationtaskstoppedwaiter)
    """

    def wait(
        self,
        Filters: List[FilterTypeDef] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WithoutSettings: bool = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationTaskStoppedWaiter)
        [Show boto3-stubs documentation](./waiters.md#replicationtaskstopped)
        """


class TestConnectionSucceedsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.test_connection_succeeds)[Show boto3-stubs documentation](./waiters.md#testconnectionsucceedswaiter)
    """

    def wait(
        self,
        Filters: List[FilterTypeDef] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/dms.html#DatabaseMigrationService.Waiter.TestConnectionSucceedsWaiter)
        [Show boto3-stubs documentation](./waiters.md#testconnectionsucceeds)
        """
