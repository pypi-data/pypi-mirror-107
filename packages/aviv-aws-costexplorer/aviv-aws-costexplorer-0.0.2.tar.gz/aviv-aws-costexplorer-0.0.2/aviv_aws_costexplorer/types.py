import typing

CAUTimePeriod = typing.Dict[typing.Literal['Start', 'End'], str]
CAUGranularity = typing.Literal['MONTHLY', 'DAILY', 'HOURLY']

# AWS CostExplorer API protos
MatchOptions = typing.Literal['EQUALS', 'STARTS_WITH', 'ENDS_WITH', 'CONTAINS', 'CASE_SENSITIVE', 'CASE_INSENSITIVE']
DimensionsKeys = typing.Literal['SERVICE', 'RECORD_TYPE', 'REGION']
RECORD_TYPE_DIMENSIONS = ["Credit", "Refund", "Upfront", "Support"]
# RECORD_TYPE_DIMENSIONS = typing.List[typing.Literal["Credit", "Refund", "Upfront", "Support"]]
GroupByTypes = typing.Literal['TAG', 'DIMENSION']
CAUMetrics = typing.List[typing.Literal['AmortizedCost', 'BlendedCost', 'NetAmortizedCost', 'NetUnblendedCost', 'NormalizedUsageAmount', 'UnblendedCost', 'UsageQuantity']]
CAUFilter = typing.Dict[typing.Literal['Or', 'And', 'Not'], dict]
CAUProps = dict(
    Granularity=CAUGranularity,
    TimePeriod=typing.Dict[typing.Literal['Start', 'End'], str],
    Filter=CAUFilter,
    Metrics=CAUMetrics,
    GroupBy=list,
    NextPageToken=str
)

# Set to Max history time CAU
CAUDefaultPeriods = dict(
    HOURLY=dict(days=14),
    DAILY=dict(days=365),
    MONTHLY=dict(months=12)
)