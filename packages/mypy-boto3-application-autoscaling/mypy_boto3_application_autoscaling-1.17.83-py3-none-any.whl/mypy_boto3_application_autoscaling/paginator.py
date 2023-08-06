"""
Type annotations for application-autoscaling service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_application_autoscaling import ApplicationAutoScalingClient
    from mypy_boto3_application_autoscaling.paginator import (
        DescribeScalableTargetsPaginator,
        DescribeScalingActivitiesPaginator,
        DescribeScalingPoliciesPaginator,
        DescribeScheduledActionsPaginator,
    )

    client: ApplicationAutoScalingClient = boto3.client("application-autoscaling")

    describe_scalable_targets_paginator: DescribeScalableTargetsPaginator = client.get_paginator("describe_scalable_targets")
    describe_scaling_activities_paginator: DescribeScalingActivitiesPaginator = client.get_paginator("describe_scaling_activities")
    describe_scaling_policies_paginator: DescribeScalingPoliciesPaginator = client.get_paginator("describe_scaling_policies")
    describe_scheduled_actions_paginator: DescribeScheduledActionsPaginator = client.get_paginator("describe_scheduled_actions")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .literals import ScalableDimensionType, ServiceNamespaceType
from .type_defs import (
    DescribeScalableTargetsResponseTypeDef,
    DescribeScalingActivitiesResponseTypeDef,
    DescribeScalingPoliciesResponseTypeDef,
    DescribeScheduledActionsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeScalableTargetsPaginator",
    "DescribeScalingActivitiesPaginator",
    "DescribeScalingPoliciesPaginator",
    "DescribeScheduledActionsPaginator",
)


class DescribeScalableTargetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/application-autoscaling.html#ApplicationAutoScaling.Paginator.DescribeScalableTargets)[Show boto3-stubs documentation](./paginators.md#describescalabletargetspaginator)
    """

    def paginate(
        self,
        ServiceNamespace: ServiceNamespaceType,
        ResourceIds: List[str] = None,
        ScalableDimension: ScalableDimensionType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeScalableTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/application-autoscaling.html#ApplicationAutoScaling.Paginator.DescribeScalableTargets.paginate)
        [Show boto3-stubs documentation](./paginators.md#describescalabletargetspaginator)
        """


class DescribeScalingActivitiesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/application-autoscaling.html#ApplicationAutoScaling.Paginator.DescribeScalingActivities)[Show boto3-stubs documentation](./paginators.md#describescalingactivitiespaginator)
    """

    def paginate(
        self,
        ServiceNamespace: ServiceNamespaceType,
        ResourceId: str = None,
        ScalableDimension: ScalableDimensionType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeScalingActivitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/application-autoscaling.html#ApplicationAutoScaling.Paginator.DescribeScalingActivities.paginate)
        [Show boto3-stubs documentation](./paginators.md#describescalingactivitiespaginator)
        """


class DescribeScalingPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/application-autoscaling.html#ApplicationAutoScaling.Paginator.DescribeScalingPolicies)[Show boto3-stubs documentation](./paginators.md#describescalingpoliciespaginator)
    """

    def paginate(
        self,
        ServiceNamespace: ServiceNamespaceType,
        PolicyNames: List[str] = None,
        ResourceId: str = None,
        ScalableDimension: ScalableDimensionType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeScalingPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/application-autoscaling.html#ApplicationAutoScaling.Paginator.DescribeScalingPolicies.paginate)
        [Show boto3-stubs documentation](./paginators.md#describescalingpoliciespaginator)
        """


class DescribeScheduledActionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/application-autoscaling.html#ApplicationAutoScaling.Paginator.DescribeScheduledActions)[Show boto3-stubs documentation](./paginators.md#describescheduledactionspaginator)
    """

    def paginate(
        self,
        ServiceNamespace: ServiceNamespaceType,
        ScheduledActionNames: List[str] = None,
        ResourceId: str = None,
        ScalableDimension: ScalableDimensionType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeScheduledActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/application-autoscaling.html#ApplicationAutoScaling.Paginator.DescribeScheduledActions.paginate)
        [Show boto3-stubs documentation](./paginators.md#describescheduledactionspaginator)
        """
