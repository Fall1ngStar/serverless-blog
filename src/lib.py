"""
lib

Common functions and classes for the project
"""
import os
from datetime import datetime
import json
from dataclasses import dataclass, field
from functools import wraps
from typing import List
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Key


def dump_result(result, status_code=200):
    """
    Prepare result as an API Gateway response with corresponding headers
    """
    return {
        'statusCode': status_code,
        'body': json.dumps(result, default=lambda x: x.__dict__),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        }
    }


@dataclass
class ApiError(Exception):
    """
    Represent an API error
    """
    result: object = field(default_factory=lambda: dict(error='Internal server error'))
    status_code: int = field(default=500)


@dataclass
class ConfigError(ApiError):
    """
    Represent a config error
    """
    missing_key: str = field(default='')


def handle_error(func):
    """
    Handle errors that can occur during lambda processing
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper for the decorated function
        """
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
        except Exception:
            return dump_result(
                result=dict(error='Internal server error'),
                status_code=500
            )

    return wrapper


class DynamoClient:
    """
    Dynamo client with configured table property
    """

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
        """
        Transform a DynamoDB item into a Post
        """
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
    """
    Handle model operation for posts
    """

    def page(self, page_number=0):
        """
        Return elements for the corresponding page_number, with the surrounding pages
        """
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
        """
        Get a post by its post_id
        """
        return Post.from_ddb(self.table.get_item(Key=dict(post_id=post_id))['Item'])

    def create(self, author, title, content):
        post_id = str(uuid4())
        self.table.put_item(Item=dict(
            post_id=post_id,
            create_date=datetime.now().isoformat(),
            type='post',
            author=author,
            title=title,
            content=content,
        ))
        return post_id

    def delete(self, post_id):
        """
        Delete a post by its post_id
        """
        self.table.delete_item(Key=dict(post_id=post_id))

    @staticmethod
    def __generate_pages(keys, page_number):
        """
        Generate pages for the given page_numbers with the keys array
        """
        count = len(keys)
        page_count = (count // 5)
        if count % 5 != 0:
            page_count += 1
        page_indexes = [*range(page_count)]
        page_slice = page_indexes[max(page_number - 2, 0):page_number + 3]
        begin, end = [], []
        if page_slice[0] != 0:
            begin = [Page('1', 'btn btn-secondary', '/?page=1'),
                     Page('...', 'btn btn-secondary disabled', '#')]
        if page_slice[-1] != page_count - 1:
            end = [Page('...', 'btn btn-secondary disabled', '#'),
                   Page(f'{page_count}', 'btn btn-secondary', f'/?page={page_count}')]
        mapped_pages = [
            Page(f'{index + 1}', 'btn btn-secondary' + (' active' if index == page_number else ''),
                 f'/?page={index + 1}')
            for index in page_slice]

        return begin + mapped_pages + end

    def __get_all_keys(self):
        """
        Get all keys in DynamoDB Table
        """
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


def with_env(func):
    """
    Isolate environments variable for the execution of the given function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper for the decorated function
        """
        original = dict(os.environ)
        try:
            result = func(*args, **kwargs)
        finally:
            os.environ = original
        return result

    return wrapper
