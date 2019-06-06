"""
create_post
"""
from src.lib import dump_result, handle_error


@handle_error
def handler(event, _context):
    """
    Handler for the create_post Lambda function
    """

    return dump_result('Post created', status_code=201)
