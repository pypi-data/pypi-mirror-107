"""
Type annotations for mediaconnect service client waiters.

[Open documentation](./waiters.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_mediaconnect import MediaConnectClient
    from mypy_boto3_mediaconnect.waiter import (
        FlowActiveWaiter,
        FlowDeletedWaiter,
        FlowStandbyWaiter,
    )

    client: MediaConnectClient = boto3.client("mediaconnect")

    flow_active_waiter: FlowActiveWaiter = client.get_waiter("flow_active")
    flow_deleted_waiter: FlowDeletedWaiter = client.get_waiter("flow_deleted")
    flow_standby_waiter: FlowStandbyWaiter = client.get_waiter("flow_standby")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("FlowActiveWaiter", "FlowDeletedWaiter", "FlowStandbyWaiter")

class FlowActiveWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediaconnect.html#MediaConnect.Waiter.flow_active)[Show boto3-stubs documentation](./waiters.md#flowactivewaiter)
    """

    def wait(self, FlowArn: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowActiveWaiter)
        [Show boto3-stubs documentation](./waiters.md#flowactive)
        """

class FlowDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediaconnect.html#MediaConnect.Waiter.flow_deleted)[Show boto3-stubs documentation](./waiters.md#flowdeletedwaiter)
    """

    def wait(self, FlowArn: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowDeletedWaiter)
        [Show boto3-stubs documentation](./waiters.md#flowdeleted)
        """

class FlowStandbyWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediaconnect.html#MediaConnect.Waiter.flow_standby)[Show boto3-stubs documentation](./waiters.md#flowstandbywaiter)
    """

    def wait(self, FlowArn: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.79/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowStandbyWaiter)
        [Show boto3-stubs documentation](./waiters.md#flowstandby)
        """
