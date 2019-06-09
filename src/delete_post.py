"""
delete_post
"""
from src.lib import dump_result, handle_error, PostModel


@handle_error
def handler(event, _context):
    """
    Handler for the delete_post Lambda function
    """
    model = PostModel()
    model.delete(event['pathParameters']['id'])
    return dump_result('Post deleted')
