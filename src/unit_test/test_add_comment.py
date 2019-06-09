"""
test_add_comment

Unit tests for the add_comment module
"""
from unittest.mock import patch
from src import add_comment


def test_handler():
    """
    Test for the handler function
    """
    event = {
        'pathParameters': {
            'id': 'id'
        },
        'body': '{"content": "content"}',
    }
    expected = {
        'statusCode': 201,
        'body': '"Comment created"',
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
    }
    with patch('src.add_comment.PostModel'):
        result = add_comment.handler(event, None)
        assert result == expected
