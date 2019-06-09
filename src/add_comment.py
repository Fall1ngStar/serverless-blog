"""
add_comment
"""
import json
from datetime import datetime
from src.lib import dump_result, handle_error, PostModel


@handle_error
def handler(event, _context):
    """
    Handler for the add_comment Lambda function
    """
    post_id = event['pathParameters']['id']
    print(event['body'])
    comment_content = json.loads(event['body'])['content']
    PostModel().table.update_item(
        Key=dict(post_id=post_id),
        UpdateExpression='set comments = list_append(:comment, if_not_exists(comments, :empty_list))',
        ExpressionAttributeValues={
            ':empty_list': [],
            ':comment': [{
                'content': comment_content,
                'create_date': datetime.now().isoformat()
            }]
        }
    )
    return dump_result('Comment created', status_code=201)
