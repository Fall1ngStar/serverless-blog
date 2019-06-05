"""
get_post
"""
from src.lib import dump_result, handle_error


@handle_error
def handler(event, _context):
    """
    Handler for the get_post Lambda function
    """
    return dump_result({
        'title': 'test',
        'author': 'test',
        'body': 'test'
    })
