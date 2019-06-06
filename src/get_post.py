"""
get_post
"""
from src.lib import dump_result, handle_error, PostModel


@handle_error
def handler(event, _context):
    """
    Handler for the get_post Lambda function
    """
    model = PostModel()
    post = model.id(event['pathParameters']['id'])
    return dump_result(post)
