"""
Type annotations for xray service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_xray import XRayClient
    from mypy_boto3_xray.paginator import (
        BatchGetTracesPaginator,
        GetGroupsPaginator,
        GetSamplingRulesPaginator,
        GetSamplingStatisticSummariesPaginator,
        GetServiceGraphPaginator,
        GetTimeSeriesServiceStatisticsPaginator,
        GetTraceGraphPaginator,
        GetTraceSummariesPaginator,
    )

    client: XRayClient = boto3.client("xray")

    batch_get_traces_paginator: BatchGetTracesPaginator = client.get_paginator("batch_get_traces")
    get_groups_paginator: GetGroupsPaginator = client.get_paginator("get_groups")
    get_sampling_rules_paginator: GetSamplingRulesPaginator = client.get_paginator("get_sampling_rules")
    get_sampling_statistic_summaries_paginator: GetSamplingStatisticSummariesPaginator = client.get_paginator("get_sampling_statistic_summaries")
    get_service_graph_paginator: GetServiceGraphPaginator = client.get_paginator("get_service_graph")
    get_time_series_service_statistics_paginator: GetTimeSeriesServiceStatisticsPaginator = client.get_paginator("get_time_series_service_statistics")
    get_trace_graph_paginator: GetTraceGraphPaginator = client.get_paginator("get_trace_graph")
    get_trace_summaries_paginator: GetTraceSummariesPaginator = client.get_paginator("get_trace_summaries")
    ```
"""
from datetime import datetime
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .literals import TimeRangeTypeType
from .type_defs import (
    BatchGetTracesResultTypeDef,
    GetGroupsResultTypeDef,
    GetSamplingRulesResultTypeDef,
    GetSamplingStatisticSummariesResultTypeDef,
    GetServiceGraphResultTypeDef,
    GetTimeSeriesServiceStatisticsResultTypeDef,
    GetTraceGraphResultTypeDef,
    GetTraceSummariesResultTypeDef,
    PaginatorConfigTypeDef,
    SamplingStrategyTypeDef,
)

__all__ = (
    "BatchGetTracesPaginator",
    "GetGroupsPaginator",
    "GetSamplingRulesPaginator",
    "GetSamplingStatisticSummariesPaginator",
    "GetServiceGraphPaginator",
    "GetTimeSeriesServiceStatisticsPaginator",
    "GetTraceGraphPaginator",
    "GetTraceSummariesPaginator",
)


class BatchGetTracesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.BatchGetTraces)[Show boto3-stubs documentation](./paginators.md#batchgettracespaginator)
    """

    def paginate(
        self, TraceIds: List[str], PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[BatchGetTracesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.BatchGetTraces.paginate)
        [Show boto3-stubs documentation](./paginators.md#batchgettracespaginator)
        """


class GetGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetGroups)[Show boto3-stubs documentation](./paginators.md#getgroupspaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[GetGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetGroups.paginate)
        [Show boto3-stubs documentation](./paginators.md#getgroupspaginator)
        """


class GetSamplingRulesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetSamplingRules)[Show boto3-stubs documentation](./paginators.md#getsamplingrulespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[GetSamplingRulesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetSamplingRules.paginate)
        [Show boto3-stubs documentation](./paginators.md#getsamplingrulespaginator)
        """


class GetSamplingStatisticSummariesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetSamplingStatisticSummaries)[Show boto3-stubs documentation](./paginators.md#getsamplingstatisticsummariespaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[GetSamplingStatisticSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetSamplingStatisticSummaries.paginate)
        [Show boto3-stubs documentation](./paginators.md#getsamplingstatisticsummariespaginator)
        """


class GetServiceGraphPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetServiceGraph)[Show boto3-stubs documentation](./paginators.md#getservicegraphpaginator)
    """

    def paginate(
        self,
        StartTime: datetime,
        EndTime: datetime,
        GroupName: str = None,
        GroupARN: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[GetServiceGraphResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetServiceGraph.paginate)
        [Show boto3-stubs documentation](./paginators.md#getservicegraphpaginator)
        """


class GetTimeSeriesServiceStatisticsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetTimeSeriesServiceStatistics)[Show boto3-stubs documentation](./paginators.md#gettimeseriesservicestatisticspaginator)
    """

    def paginate(
        self,
        StartTime: datetime,
        EndTime: datetime,
        GroupName: str = None,
        GroupARN: str = None,
        EntitySelectorExpression: str = None,
        Period: int = None,
        ForecastStatistics: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[GetTimeSeriesServiceStatisticsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetTimeSeriesServiceStatistics.paginate)
        [Show boto3-stubs documentation](./paginators.md#gettimeseriesservicestatisticspaginator)
        """


class GetTraceGraphPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetTraceGraph)[Show boto3-stubs documentation](./paginators.md#gettracegraphpaginator)
    """

    def paginate(
        self, TraceIds: List[str], PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[GetTraceGraphResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetTraceGraph.paginate)
        [Show boto3-stubs documentation](./paginators.md#gettracegraphpaginator)
        """


class GetTraceSummariesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetTraceSummaries)[Show boto3-stubs documentation](./paginators.md#gettracesummariespaginator)
    """

    def paginate(
        self,
        StartTime: datetime,
        EndTime: datetime,
        TimeRangeType: TimeRangeTypeType = None,
        Sampling: bool = None,
        SamplingStrategy: SamplingStrategyTypeDef = None,
        FilterExpression: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[GetTraceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.83/reference/services/xray.html#XRay.Paginator.GetTraceSummaries.paginate)
        [Show boto3-stubs documentation](./paginators.md#gettracesummariespaginator)
        """
