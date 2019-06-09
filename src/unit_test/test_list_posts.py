"""
test_list_posts

Unit tests for the list_posts module
"""
from unittest.mock import patch

from src import list_posts


def test_handler():
    """
    Test for the handler function
    """
    event = {
        'queryStringParameters': {
            'page': '3'
        }
    }
    expected = {
        'statusCode': 200,
        'body': '{"pages": [], "posts": []}',
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
    }
    with patch('src.list_posts.PostModel') as model:
        model().page.return_value = {
            'pages': [],
            'posts': [],
        }
        result = list_posts.handler(event, None)
        assert result == expected
