"""
test_delete_post

Unit tests for the delete_post module
"""
from unittest.mock import patch

from src import delete_post


def test_handler():
    """
    Test for the handler function
    """
    event = {
        'pathParameters': {
            'id': 'id'
        },
    }
    expected = {
        'statusCode': 200,
        'body': '"Post deleted"',
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
    }
    with patch('src.delete_post.PostModel') as model:
        result = delete_post.handler(event, None)
        model().delete.assert_called_with('id')
        assert result == expected
