import os
import logging
import typing
import boto3
import botocore
import pandas as pd
import awswrangler as wr
from . import (
    types,
    base
)

BUCKET = os.environ.get("BUCKET")


class DataStore(base.AWSClient):
    _bucket: str
    _database: str
    boto3_session = None

    def __init__(self, *, bucket: str=None, database: str=None, role_arn: str=None) -> None:
        super().__init__()
        if role_arn:
            self.boto3_session = self.session(role_arn=role_arn, role_session_name='Reporter', set_as_detault=True)
            logging.warning(f"Set boto3 session ({self.boto3_session})")
        self.bucket = bucket
        self.database = database

    @property
    def bucket(self):
        return self._bucket

    @bucket.setter
    def bucket(self, name: str):
        self._bucket = name

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, name: str):
        self._database = name
        if name not in self.databases():
            logging.error(f"Database '{name}' not found")
            confirm = input("Wanna create it? [y/N]")
            if confirm == 'y':
                self.create_database(name=name)
                logging.warning(f"Created database: {name}")

    def databases(self) -> list:
        dbs = wr.catalog.databases(boto3_session=self.boto3_session)
        return list(dbs.Database)

    def create_database(self, name: str):
        return wr.catalog.create_database(name, boto3_session=self.boto3_session)

    def tables(self):
        return wr.catalog.tables(database=self.database, boto3_session=self.boto3_session)

    def to_parquet(
            self,
            data: typing.Union[dict, list, pd.DataFrame],
            path: str='data',
            database: str=None,
            table: str=None,
            **kwargs) -> dict:
        """Save data as parquet, obviously doh!
        """
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)

        if self.bucket:
            path = f"s3://{self.bucket}/{path}"
        if database:
            self.database = database
        path += f"{self.database}/{table}"

        if not path.startswith('s3://'):
            return data.to_parquet(path=path) #, engine='pyarrow'

        return wr.s3.to_parquet(
            df=data,
            path=path,
            dataset=True,
            database=self.database,
            table=table,
            **kwargs
        )

    def read_parquet(self, path: str, **kwargs) -> pd.DataFrame:
        if not path.startswith('s3://'):
            pd.read_parquet(path=path, engine='pyarrow')
        return wr.s3.read_parquet(
            path=path,
            dataset=True,
            **kwargs
        )

    def read_athena(self, query: str, **kwargs) -> pd.DataFrame:
        return wr.athena.read_sql_query(
            query,
            database=self.database,
            boto3_session=self.boto3_session,
            **kwargs
        )

    # TMP help / clean later (yeah it's bad to leave trash in code...)
    @staticmethod
    def pd_format(data: pd.DataFrame):
        # pick first item and lowercase it
        granularity: str = data.Granularity[0].lower()

        # cast as string
        data['AccountId'] = data.AccountId.astype('string')

        # date (dd/mm/yyyy) and time (dd/mm/yyyy hh:mm:ss)
        data['Start'] = pd.to_datetime(data['Start'])
        if granularity == 'hourly':
            data['Start'] = data['Start'].dt.date

        # From datetime to string format
        data['Period'] = data.Start.astype('string')
        data['Period'] = data.Period.str.replace('-', '')
        if granularity == 'monthly':
            data['Period'] = data.Period.str[:-2]
        data['Period'] = data.Period.astype('int')
