"""
Type annotations for elbv2 service client waiters.

[Open documentation](./waiters.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_elbv2 import ElasticLoadBalancingv2Client
    from mypy_boto3_elbv2.waiter import (
        LoadBalancerAvailableWaiter,
        LoadBalancerExistsWaiter,
        LoadBalancersDeletedWaiter,
        TargetDeregisteredWaiter,
        TargetInServiceWaiter,
    )

    client: ElasticLoadBalancingv2Client = boto3.client("elbv2")

    load_balancer_available_waiter: LoadBalancerAvailableWaiter = client.get_waiter("load_balancer_available")
    load_balancer_exists_waiter: LoadBalancerExistsWaiter = client.get_waiter("load_balancer_exists")
    load_balancers_deleted_waiter: LoadBalancersDeletedWaiter = client.get_waiter("load_balancers_deleted")
    target_deregistered_waiter: TargetDeregisteredWaiter = client.get_waiter("target_deregistered")
    target_in_service_waiter: TargetInServiceWaiter = client.get_waiter("target_in_service")
    ```
"""
from typing import List

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import TargetDescriptionTypeDef, WaiterConfigTypeDef

__all__ = (
    "LoadBalancerAvailableWaiter",
    "LoadBalancerExistsWaiter",
    "LoadBalancersDeletedWaiter",
    "TargetDeregisteredWaiter",
    "TargetInServiceWaiter",
)


class LoadBalancerAvailableWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.load_balancer_available)[Show boto3-stubs documentation](./waiters.md#loadbalanceravailablewaiter)
    """

    def wait(
        self,
        LoadBalancerArns: List[str] = None,
        Names: List[str] = None,
        Marker: str = None,
        PageSize: int = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancerAvailableWaiter)
        [Show boto3-stubs documentation](./waiters.md#loadbalanceravailable)
        """


class LoadBalancerExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.load_balancer_exists)[Show boto3-stubs documentation](./waiters.md#loadbalancerexistswaiter)
    """

    def wait(
        self,
        LoadBalancerArns: List[str] = None,
        Names: List[str] = None,
        Marker: str = None,
        PageSize: int = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancerExistsWaiter)
        [Show boto3-stubs documentation](./waiters.md#loadbalancerexists)
        """


class LoadBalancersDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.load_balancers_deleted)[Show boto3-stubs documentation](./waiters.md#loadbalancersdeletedwaiter)
    """

    def wait(
        self,
        LoadBalancerArns: List[str] = None,
        Names: List[str] = None,
        Marker: str = None,
        PageSize: int = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancersDeletedWaiter)
        [Show boto3-stubs documentation](./waiters.md#loadbalancersdeleted)
        """


class TargetDeregisteredWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.target_deregistered)[Show boto3-stubs documentation](./waiters.md#targetderegisteredwaiter)
    """

    def wait(
        self,
        TargetGroupArn: str,
        Targets: List["TargetDescriptionTypeDef"] = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.TargetDeregisteredWaiter)
        [Show boto3-stubs documentation](./waiters.md#targetderegistered)
        """


class TargetInServiceWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.target_in_service)[Show boto3-stubs documentation](./waiters.md#targetinservicewaiter)
    """

    def wait(
        self,
        TargetGroupArn: str,
        Targets: List["TargetDescriptionTypeDef"] = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.TargetInServiceWaiter)
        [Show boto3-stubs documentation](./waiters.md#targetinservice)
        """
