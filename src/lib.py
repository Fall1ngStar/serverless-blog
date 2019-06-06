import os
from datetime import datetime
import json
from dataclasses import dataclass, field
from typing import List
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Key


def dump_result(result, status_code=200):
    return {
        'statusCode': status_code,
        'body': json.dumps(result, default=lambda x: x.__dict__),
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
    def __init__(self):
        self._table = None

    @property
    def table(self):
        if not self._table:
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


@dataclass
class Post:
    post_id: str
    author: str
    title: str
    content: str
    create_date: datetime
    comments: List[Comment] = field(default_factory=list)

    @staticmethod
    def from_ddb(item):
        comments = [
            Comment(content=c['content'], create_date=c['create_date'])
            for c in item.get('comments', [])]
        return Post(
            post_id=item.get('post_id', ''),
            author=item.get('author', ''),
            title=item.get('title', ''),
            content=item.get('content', ''),
            create_date=item.get('create_date', ''),
            comments=comments,
        )


@dataclass
class Page:
    content: str
    classes: str
    url: str


class PostModel(DynamoClient):
    def page(self, page_number=0):
        self.table.load()
        keys = self.__get_all_keys()
        selected_keys = keys[page_number * 5: (page_number + 1) * 5]
        posts = [Post.from_ddb(self.table.get_item(Key=dict(post_id=key))['Item'])
                 for key in selected_keys]
        pages = self.__generate_pages(keys, page_number)
        return dict(
            posts=posts,
            pages=pages,
        )

    def id(self, post_id):
        return Post.from_ddb(self.table.get_item(Key=dict(post_id=post_id))['Item'])

    def create(self, author, title, content):
        self.table.put_item(Item=dict(
            post_id=str(uuid4()),
            create_date=datetime.now().isoformat(),
            type='post',
            author=author,
            title=title,
            content=content,
        ))

    def delete(self, post_id):
        self.table.delete_item(Key=dict(post_id=post_id))

    @staticmethod
    def __generate_pages(keys, page_number):
        count = len(keys)
        page_count = (count // 5) + 1
        page_indexes = [*range(page_count)]
        page_slice = page_indexes[max(page_number - 2, 0):page_number + 3]
        begin, end = [], []
        if page_slice[0] != 0:
            begin = [Page('1', 'btn btn-secondary', '/posts/?page=1'),
                     Page('...', 'btn btn-secondary disabled', '#')]
        if page_slice[-1] != page_count - 1:
            end = [Page('...', 'btn btn-secondary disabled', '#'),
                   Page(f'{page_count}', 'btn btn-secondary', f'/posts/?page={page_count}')]
        mapped_pages = [Page(f'{index + 1}', 'btn btn-secondary', f'/posts/?page={index + 1}')
                        for index in page_slice]

        return begin + mapped_pages + end

    def __get_all_keys(self):
        total = []
        has_next = True
        last_key = None
        while has_next:
            params = dict(
                IndexName='type-date-index',
                KeyConditionExpression=Key('type').eq('post'),
                ScanIndexForward=False,
                ProjectionExpression='post_id',
            )
            if last_key:
                params['ExclusiveStartKey'] = last_key
            response = self.table.query(**params)
            total += [post['post_id'] for post in response['Items']]
            last_key = response.get('LastEvaluatedKey', None)
            has_next = 'LastEvaluatedKey' in response
        return total
