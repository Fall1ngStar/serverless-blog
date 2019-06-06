"""
list_posts
"""
from src.lib import dump_result, handle_error, PostModel


@handle_error
def handler(event, _context):
    """
    Handler for the list_posts Lambda function
    """
    params = event['queryStringParameters']
    if params:
        page = int(params.get('page', '1')) - 1
    else:
        page = 0
    model = PostModel()
    return dump_result(model.page(page))
