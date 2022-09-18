from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

class Comment:
    def __init__(self, data:dict):
        self.id = data['id']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    # STATIC METHODS
    def validate_comment(data:dict):
        is_valid = True
        if len(data.get('content')) < 1:
            is_valid = False
            flash(u'Comment is too short! Cannot be blank.', 'comment')
        return is_valid
    
    def parse_comment(data:dict):
        parsed_data = {
            'id': data.get('id'),
            'user_id': data.get('user_id'),
            'post_id': data.get('post_id'),
            'content': data.get('content'),
        }

    # CLASS METHODS
    @classmethod
    def create(cls, data:dict):
        query = '''
        INSERT INTO comments (user_id, post_id, content)
        VALUES (%(user_id)s, %(post_id)s, %(content)s)
        '''
        return connectToMySQL('dojo_wall').query_db(query, data)