import os
from datetime import datetime
import json
from dataclasses import dataclass, field
from typing import List
import boto3


def dump_result(result, status_code=200):
    return {
        'statusCode': status_code,
        'body': json.dumps(result),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Credentials": True,
        }
    }


@dataclass
class ApiError(Exception):
    result: object = field(default_factory=lambda: dict(error='Internal server error'))
    status_code: int = field(default=500)


@dataclass
class ConfigError(ApiError):
    missing_key: str = field(default='')


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConfigError as error:
            print(f'Missing variale "{error.missing_key}" in function environment')
            return dump_result(
                result=dict(error='Internal server error'),
                status_code=500
            )
        except ApiError as error:
            return dump_result(
                result=error.result,
                status_code=error.status_code,
            )
    return wrapper


class DynamoClient:
    _table: None

    @property
    def table(self):
        if not self.table:
            resource = boto3.resource('dynamodb')
            try:
                self._table = resource.Table(os.environ['DYNAMO_TABLE'])
            except KeyError:
                raise ConfigError(missing_key='DYNAMO_TABLE')
        return self._table


@dataclass
class Comment:
    content: str
    create_date: datetime


class Post(DynamoClient):
    post_id: str
    author: str
    title: str
    content: str
    create_date: datetime
    comments: List[Comment] = []

    @classmethod
    def from_id(cls, post_id):
        pass
