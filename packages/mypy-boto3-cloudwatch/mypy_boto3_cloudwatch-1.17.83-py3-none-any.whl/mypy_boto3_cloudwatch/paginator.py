"""
Type annotations for cloudwatch service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_cloudwatch import CloudWatchClient
    from mypy_boto3_cloudwatch.paginator import (
        DescribeAlarmHistoryPaginator,
        DescribeAlarmsPaginator,
        GetMetricDataPaginator,
        ListDashboardsPaginator,
        ListMetricsPaginator,
    )

    client: CloudWatchClient = boto3.client("cloudwatch")

    describe_alarm_history_paginator: DescribeAlarmHistoryPaginator = client.get_paginator("describe_alarm_history")
    describe_alarms_paginator: DescribeAlarmsPaginator = client.get_paginator("describe_alarms")
    get_metric_data_paginator: GetMetricDataPaginator = client.get_paginator("get_metric_data")
    list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
    list_metrics_paginator: ListMetricsPaginator = client.get_paginator("list_metrics")
    ```
"""
import sys
from datetime import datetime
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .literals import AlarmTypeType, HistoryItemTypeType, ScanByType, StateValueType
from .type_defs import (
    DescribeAlarmHistoryOutputTypeDef,
    DescribeAlarmsOutputTypeDef,
    DimensionFilterTypeDef,
    GetMetricDataOutputTypeDef,
    LabelOptionsTypeDef,
    ListDashboardsOutputTypeDef,
    ListMetricsOutputTypeDef,
    MetricDataQueryTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "DescribeAlarmHistoryPaginator",
    "DescribeAlarmsPaginator",
    "GetMetricDataPaginator",
    "ListDashboardsPaginator",
    "ListMetricsPaginator",
)


class DescribeAlarmHistoryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudwatch.html#CloudWatch.Paginator.DescribeAlarmHistory)[Show boto3-stubs documentation](./paginators.md#describealarmhistorypaginator)
    """

    def paginate(
        self,
        AlarmName: str = None,
        AlarmTypes: List[AlarmTypeType] = None,
        HistoryItemType: HistoryItemTypeType = None,
        StartDate: datetime = None,
        EndDate: datetime = None,
        ScanBy: ScanByType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeAlarmHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudwatch.html#CloudWatch.Paginator.DescribeAlarmHistory.paginate)
        [Show boto3-stubs documentation](./paginators.md#describealarmhistorypaginator)
        """


class DescribeAlarmsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudwatch.html#CloudWatch.Paginator.DescribeAlarms)[Show boto3-stubs documentation](./paginators.md#describealarmspaginator)
    """

    def paginate(
        self,
        AlarmNames: List[str] = None,
        AlarmNamePrefix: str = None,
        AlarmTypes: List[AlarmTypeType] = None,
        ChildrenOfAlarmName: str = None,
        ParentsOfAlarmName: str = None,
        StateValue: StateValueType = None,
        ActionPrefix: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeAlarmsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudwatch.html#CloudWatch.Paginator.DescribeAlarms.paginate)
        [Show boto3-stubs documentation](./paginators.md#describealarmspaginator)
        """


class GetMetricDataPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudwatch.html#CloudWatch.Paginator.GetMetricData)[Show boto3-stubs documentation](./paginators.md#getmetricdatapaginator)
    """

    def paginate(
        self,
        MetricDataQueries: List["MetricDataQueryTypeDef"],
        StartTime: datetime,
        EndTime: datetime,
        ScanBy: ScanByType = None,
        LabelOptions: LabelOptionsTypeDef = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[GetMetricDataOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudwatch.html#CloudWatch.Paginator.GetMetricData.paginate)
        [Show boto3-stubs documentation](./paginators.md#getmetricdatapaginator)
        """


class ListDashboardsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudwatch.html#CloudWatch.Paginator.ListDashboards)[Show boto3-stubs documentation](./paginators.md#listdashboardspaginator)
    """

    def paginate(
        self, DashboardNamePrefix: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListDashboardsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudwatch.html#CloudWatch.Paginator.ListDashboards.paginate)
        [Show boto3-stubs documentation](./paginators.md#listdashboardspaginator)
        """


class ListMetricsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudwatch.html#CloudWatch.Paginator.ListMetrics)[Show boto3-stubs documentation](./paginators.md#listmetricspaginator)
    """

    def paginate(
        self,
        Namespace: str = None,
        MetricName: str = None,
        Dimensions: List[DimensionFilterTypeDef] = None,
        RecentlyActive: Literal["PT3H"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListMetricsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/cloudwatch.html#CloudWatch.Paginator.ListMetrics.paginate)
        [Show boto3-stubs documentation](./paginators.md#listmetricspaginator)
        """
