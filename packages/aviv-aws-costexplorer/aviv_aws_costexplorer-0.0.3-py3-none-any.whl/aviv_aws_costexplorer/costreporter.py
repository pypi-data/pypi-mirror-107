import os
import logging
import datetime
from dateutil.relativedelta import relativedelta
from . import (
    costexplorer,
    filters,
    types
)

AWS_FINOPS_ROLE = os.environ.get('AWS_FINOPS_ROLE', 'AWSFinopsCollector')

log = logging.getLogger(__name__)


class CostReporter(costexplorer.CostExplorer):
    __tags: dict = {}

    def __init__(
            self,
            *,
            role_arn: str=None,
            granularity: str='MONTHLY',
            period: relativedelta=None,
            date: datetime.datetime=None) -> None:
        """Aviv AWS Cost Reporter

        Args:
            role_arn (str, optional): [description]. Defaults to None.
            granularity (str, optional): [description]. Defaults to 'MONTHLY'.
            period (relativedelta, optional): [description]. Defaults to None.
            date (datetime.datetime, optional): [description]. Defaults to None.
        """
        super().__init__(
            role_arn=role_arn,
            granularity=granularity,
            period=period,
            date=date
        )

    @property
    def tags(self):
        if not self.__tags:
            self.__tags = self.get_tags_by_keys()
        return self.__tags

    # Data manipulations
    @staticmethod
    def _flatten_amounts(amounts: dict) -> dict:
        return dict(
            (a, float(v['Amount'])) for a, v in amounts.items()
                if isinstance(v, dict) and 'Amount' in v
        )

    @staticmethod
    def _extend_groups(record: dict, group_definitions: list=None) -> list:
        flat = list()
        base = record.copy()
        del base['Groups']
        log.debug(f"Extend: {base['Start']} with {len(record['Groups'])} records #{base['RequestId']} (g:{group_definitions})")
        for group in record['Groups']:
            g = base.copy()
            g['Key'] = group['Keys'][0]

            if len(group['Keys']) > 1:
                if len(group_definitions) == 2 and group_definitions[1]['Type']:  # == 'TAG':  # // Filter by AWS tags
                    g[group_definitions[1]['Type']] = group['Keys'][1]
                else:
                    log.info(f" Group have multiple keys definition {list(group['Keys'][1:])}")

            # Flat
            g.update(CostReporter._flatten_amounts(group['Metrics']))
            flat.append(g)
        return flat

    def stamp_record(self, record: dict, metadata: dict) -> None:
        """Augment record with critical information about what was collected.

        Args:
            record (dict): the record to augment
            metadata (dict): information about the API request (ResponseMetadata)
        """
        # Specific to cost_and_usage (CAU)
        record['Granularity'] = self.granularity
        # Save TimePeriod + RequestId
        if 'TimePeriod' in record:
            record.update(record['TimePeriod'])
            del record['TimePeriod']
            record['Period'] = record['Start'].replace('-', '')
            if record['Granularity'] == 'MONTHLY':
                record['Period'] = record['Period']
        record['RequestId'] = metadata['RequestId']

    # Calls to AWS CAU api
    def get_cost_and_usage(self, **props: types.CAUProps) -> dict:
        """Calls underlying CostExplorer.get_cost_and_usage to produce CAU records

        This method will also:
         - Extend and flatten the response ['ResultsByTime'], see: _extend_flatten_cau_record method
         - Cleanup extra ['ResponseMetadata']

        Args:
            cau_name (str, optional): A friendly, human readable, name to be added to the records. Defaults to None.

        Returns:
            dict: The CAU call response
        """
        data = super().get_cost_and_usage(**props)
        for record in data['ResultsByTime']:
            self.stamp_record(record, data['ResponseMetadata'])
            if 'Total' in record:
                record.update(CostReporter._flatten_amounts(record['Total']))
                del record['Total']
        log.info(f"Got CAU {len(data['ResultsByTime'])} datapoints for {data.keys()}")
        if 'GroupDefinitions' in data and data['GroupDefinitions']:
            log.info(f"- GroupDefinitions:{data['GroupDefinitions']}")
        if 'DimensionValueAttributes' in data and data['DimensionValueAttributes']:
            log.info(f"- DimensionValueAttributes:{data['DimensionValueAttributes']}")
        return data

    def get_cost_by(self, dimension: types.DimensionsKeys='RECORD_TYPE', tag: str=None, filter: dict=None, metrics: list=['UnblendedCost']) -> list:
        """
        Consolidate costs by AWS CAU 'dimension' (RECORD_TYPE: total/usage, SERVICE, REGION...)

        Args:
            dimension (DimensionsKeys, optional): [description]. Defaults to 'RECORD_TYPE'.
            tag (str, optional): [description]. Defaults to None.
            filter (dict, optional): [description]. Defaults to None.
            metrics (list, optional): [description]. Defaults to ['UnblendedCost'].

        Returns:
            list: [description]
        """
        groupby = [{"Type": "DIMENSION", "Key": dimension.upper()}]
        if tag:
            groupby.append({'Type': 'TAG', 'Key': tag})
            # DO NOT add this filter, or grand totals won't match!
            # filter = {'Dimensions': {'Key': 'RECORD_TYPE', 'Values': ['Usage']}}
        props = dict(
            GroupBy=groupby,
            Metrics=metrics
        )
        if filter:
            props['Filter'] = filter
        data = self.get_cost_and_usage(**props)
        # Extend/augment dataset by 'GroupDefinitions'
        edata = list()
        for dp in data['ResultsByTime']:
            dp['Dimension'] = dimension.upper()
            edata += CostReporter._extend_groups(dp, data['GroupDefinitions'])
        log.info(f"Extended {dimension} to {len(edata)} datapoints")
        return edata

    def get_tags_by_keys(self, keys: list) -> dict:
        """List AWS Tags (by name/key) which have associated values+cost for the given period.
        Ignore AWS Tags who have not been used

        Args:
            keys (list, optional): [description]

        Returns:
            dict: [description]
        """
        log.info(f"Scan tags: {keys}")
        tags = dict()
        for key in keys:
            values = self.get_tags(key)
            if len(values) > 1:  # Filter by Tags first element is always empty ['']
                tags[key] = values
        return tags

    # Helpers to get CAU basic dimensions the grand total for each of those datasets must match
    def totals(self) -> list:
        """Consolidate 'Totals' related/general costs

        Returns:
            list: costs (Usage, Tax, Credit, Refund, RI...)
        """
        data = list()
        data += self.get_cost_by(dimension='RECORD_TYPE', filter=filters.CostExplorerFilter.NoCredits())
        data += self.get_cost_by(dimension='RECORD_TYPE', filter=filters.CostExplorerFilter.CreditsOnly())
        data += self.get_cost_by(dimension='RECORD_TYPE', filter=filters.CostExplorerFilter.RefundOnly())
        data += self.get_cost_by(dimension='RECORD_TYPE', filter=filters.CostExplorerFilter.UpfrontOnly())
        return data
