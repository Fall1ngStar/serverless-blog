"""
add_comment
"""
from src.lib import dump_result, handle_error


@handle_error
def handler(event, _context):
    """
    Handler for the add_comment Lambda function
    """
    return dump_result('Comment created', status_code=201)
