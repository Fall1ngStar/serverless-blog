"""
test_get_post

Unit tests for the get_post module
"""
import os
from unittest.mock import patch

from src import get_post
from src.lib import with_env


@with_env
def test_handler():
    """
    Test for the handler function
    """
    os.environ['DYNAMO_TABLE'] = 'table'
    event = {
        'pathParameters': {
            'id': 'id'
        },
    }
    expected = {
        'statusCode': 200,
        'body': '{"post_id": "id"}',
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
    }
    with patch('src.get_post.PostModel') as model:
        model().id.return_value = {'post_id': 'id'}
        result = get_post.handler(event, None)
        model().id.assert_called_with('id')
        assert result == expected
