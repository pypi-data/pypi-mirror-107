"""
Type annotations for autoscaling service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_autoscaling import AutoScalingClient
    from mypy_boto3_autoscaling.paginator import (
        DescribeAutoScalingGroupsPaginator,
        DescribeAutoScalingInstancesPaginator,
        DescribeLaunchConfigurationsPaginator,
        DescribeLoadBalancerTargetGroupsPaginator,
        DescribeLoadBalancersPaginator,
        DescribeNotificationConfigurationsPaginator,
        DescribePoliciesPaginator,
        DescribeScalingActivitiesPaginator,
        DescribeScheduledActionsPaginator,
        DescribeTagsPaginator,
    )

    client: AutoScalingClient = boto3.client("autoscaling")

    describe_auto_scaling_groups_paginator: DescribeAutoScalingGroupsPaginator = client.get_paginator("describe_auto_scaling_groups")
    describe_auto_scaling_instances_paginator: DescribeAutoScalingInstancesPaginator = client.get_paginator("describe_auto_scaling_instances")
    describe_launch_configurations_paginator: DescribeLaunchConfigurationsPaginator = client.get_paginator("describe_launch_configurations")
    describe_load_balancer_target_groups_paginator: DescribeLoadBalancerTargetGroupsPaginator = client.get_paginator("describe_load_balancer_target_groups")
    describe_load_balancers_paginator: DescribeLoadBalancersPaginator = client.get_paginator("describe_load_balancers")
    describe_notification_configurations_paginator: DescribeNotificationConfigurationsPaginator = client.get_paginator("describe_notification_configurations")
    describe_policies_paginator: DescribePoliciesPaginator = client.get_paginator("describe_policies")
    describe_scaling_activities_paginator: DescribeScalingActivitiesPaginator = client.get_paginator("describe_scaling_activities")
    describe_scheduled_actions_paginator: DescribeScheduledActionsPaginator = client.get_paginator("describe_scheduled_actions")
    describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    ```
"""
from datetime import datetime
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ActivitiesTypeTypeDef,
    AutoScalingGroupsTypeTypeDef,
    AutoScalingInstancesTypeTypeDef,
    DescribeLoadBalancersResponseTypeDef,
    DescribeLoadBalancerTargetGroupsResponseTypeDef,
    DescribeNotificationConfigurationsAnswerTypeDef,
    FilterTypeDef,
    LaunchConfigurationsTypeTypeDef,
    PaginatorConfigTypeDef,
    PoliciesTypeTypeDef,
    ScheduledActionsTypeTypeDef,
    TagsTypeTypeDef,
)

__all__ = (
    "DescribeAutoScalingGroupsPaginator",
    "DescribeAutoScalingInstancesPaginator",
    "DescribeLaunchConfigurationsPaginator",
    "DescribeLoadBalancerTargetGroupsPaginator",
    "DescribeLoadBalancersPaginator",
    "DescribeNotificationConfigurationsPaginator",
    "DescribePoliciesPaginator",
    "DescribeScalingActivitiesPaginator",
    "DescribeScheduledActionsPaginator",
    "DescribeTagsPaginator",
)


class DescribeAutoScalingGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeAutoScalingGroups)[Show boto3-stubs documentation](./paginators.md#describeautoscalinggroupspaginator)
    """

    def paginate(
        self,
        AutoScalingGroupNames: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[AutoScalingGroupsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeAutoScalingGroups.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeautoscalinggroupspaginator)
        """


class DescribeAutoScalingInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeAutoScalingInstances)[Show boto3-stubs documentation](./paginators.md#describeautoscalinginstancespaginator)
    """

    def paginate(
        self, InstanceIds: List[str] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[AutoScalingInstancesTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeAutoScalingInstances.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeautoscalinginstancespaginator)
        """


class DescribeLaunchConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeLaunchConfigurations)[Show boto3-stubs documentation](./paginators.md#describelaunchconfigurationspaginator)
    """

    def paginate(
        self,
        LaunchConfigurationNames: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[LaunchConfigurationsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeLaunchConfigurations.paginate)
        [Show boto3-stubs documentation](./paginators.md#describelaunchconfigurationspaginator)
        """


class DescribeLoadBalancerTargetGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeLoadBalancerTargetGroups)[Show boto3-stubs documentation](./paginators.md#describeloadbalancertargetgroupspaginator)
    """

    def paginate(
        self, AutoScalingGroupName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeLoadBalancerTargetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeLoadBalancerTargetGroups.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeloadbalancertargetgroupspaginator)
        """


class DescribeLoadBalancersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeLoadBalancers)[Show boto3-stubs documentation](./paginators.md#describeloadbalancerspaginator)
    """

    def paginate(
        self, AutoScalingGroupName: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[DescribeLoadBalancersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeLoadBalancers.paginate)
        [Show boto3-stubs documentation](./paginators.md#describeloadbalancerspaginator)
        """


class DescribeNotificationConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeNotificationConfigurations)[Show boto3-stubs documentation](./paginators.md#describenotificationconfigurationspaginator)
    """

    def paginate(
        self,
        AutoScalingGroupNames: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeNotificationConfigurationsAnswerTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeNotificationConfigurations.paginate)
        [Show boto3-stubs documentation](./paginators.md#describenotificationconfigurationspaginator)
        """


class DescribePoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribePolicies)[Show boto3-stubs documentation](./paginators.md#describepoliciespaginator)
    """

    def paginate(
        self,
        AutoScalingGroupName: str = None,
        PolicyNames: List[str] = None,
        PolicyTypes: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[PoliciesTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribePolicies.paginate)
        [Show boto3-stubs documentation](./paginators.md#describepoliciespaginator)
        """


class DescribeScalingActivitiesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeScalingActivities)[Show boto3-stubs documentation](./paginators.md#describescalingactivitiespaginator)
    """

    def paginate(
        self,
        ActivityIds: List[str] = None,
        AutoScalingGroupName: str = None,
        IncludeDeletedGroups: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ActivitiesTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeScalingActivities.paginate)
        [Show boto3-stubs documentation](./paginators.md#describescalingactivitiespaginator)
        """


class DescribeScheduledActionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeScheduledActions)[Show boto3-stubs documentation](./paginators.md#describescheduledactionspaginator)
    """

    def paginate(
        self,
        AutoScalingGroupName: str = None,
        ScheduledActionNames: List[str] = None,
        StartTime: datetime = None,
        EndTime: datetime = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ScheduledActionsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeScheduledActions.paginate)
        [Show boto3-stubs documentation](./paginators.md#describescheduledactionspaginator)
        """


class DescribeTagsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeTags)[Show boto3-stubs documentation](./paginators.md#describetagspaginator)
    """

    def paginate(
        self, Filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[TagsTypeTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeTags.paginate)
        [Show boto3-stubs documentation](./paginators.md#describetagspaginator)
        """
