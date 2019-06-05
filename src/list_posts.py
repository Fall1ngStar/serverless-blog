"""
list_posts
"""
from src.lib import dump_result, handle_error


@handle_error
def handler(event, _context):
    """
    Handler for the list_posts Lambda function
    """
    return dump_result({
        'post_list': [1, 2, 3]
    })
