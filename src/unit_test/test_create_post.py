"""
test_create_post

Unit tests for the create_post module
"""
import json
from unittest.mock import patch

from src import create_post


def test_handler():
    """
    Test for the handler function
    """
    event = {
        'body': json.dumps(dict(
            author='author',
            title='title',
            content='content',
        ))
    }
    expected = {
        'statusCode': 201,
        'body': '{"post_id": "id"}',
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
    }
    with patch('src.create_post.PostModel') as model:
        model().create.return_value = 'id'
        result = create_post.handler(event, None)
        assert result == expected
