"""
create_post
"""
import json
from src.lib import dump_result, handle_error, PostModel


@handle_error
def handler(event, _context):
    """
    Handler for the create_post Lambda function
    """
    model = PostModel()
    post_id = model.create(**json.loads(event['body']))
    return dump_result({'post_id': post_id}, status_code=201)
