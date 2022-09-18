from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user, comment
from flask import flash

class Post:
    def __init__(self, data:dict):
        self.id = data['id']
        self.user_id = data['user_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.comments = []

    # STATIC METHODS HERE
    @staticmethod
    def validate_post(data:dict):
        is_valid = True
        if len(data.get('content')) < 1:
            is_valid = False
            flash(u'Your post is too short!', 'post')
        return is_valid

    def parse_data(data:dict):
        parsed_data = {
            'user_id': data.get('user_id'),
            'content': data.get('content')
        }

        return parsed_data

    #CLASS METHODS HERE
    @classmethod
    def create(cls, data:dict):
        query = '''
        INSERT INTO posts (user_id, content)
        VALUES (%(user_id)s, %(content)s);
        '''

        return connectToMySQL('dojo_wall').query_db(query,data)

    @classmethod
    def delete(cls, data:dict):
        query = '''
        DELETE FROM posts WHERE posts.id = %(id)s;
        '''
        return connectToMySQL('dojo_wall').query_db(query,data)
    @classmethod
    def get_all(cls):
        query = '''
        SELECT * FROM posts;
        '''
        results = connectToMySQL('dojo_wall').query_db(query)

        all_posts = []

        for row in results:
            all_posts.append(cls(row))
        
        return all_posts

    @classmethod
    def get_all_with_creator(cls):
        query = '''
        SELECT * FROM posts
        JOIN users ON posts.user_id = users.id
        GROUP BY posts.created_at
        ORDER BY posts.created_at DESC;
        '''
        results = connectToMySQL('dojo_wall').query_db(query)

        all_posts = []

        if results:
            for row in results:
                # create an instance of user for each post
                one_post = cls(row)

                # collect the user data from the row in each iteration
                creator_data = {
                    'id' : row.get('users.id'),
                    'first_name' : row.get('first_name'),
                    'last_name' : row.get('last_name'),
                    'email' : row.get('email'),
                    'password' : row.get('password'),
                    'created_at' : row.get('created_at'),
                    'updated_at' : row.get('updated_at')
                }

                comment_data = {
                    'i'
                }

                print(f'Creator data: {creator_data}..............................................')
                # create a user with the data aquired from the iteration
                one_creator = user.User(creator_data)
                # set the current user to the creator attribute of each post
                one_post.creator = one_creator
                # append each post to the list of posts and return the list of posts with creator
                all_posts.append(one_post)
        else:
            print('WHOOOPS! MY FOLLY')
        
        return all_posts
    
    @classmethod
    def get_all_with_creator_comments(cls):
        query = '''
        SELECT * FROM posts
        JOIN users ON posts.user_id = users.id
        LEFT JOIN comments ON posts.id = comments.post_id
        LEFT JOIN users AS comment_creator ON comments.user_id = comment_creator.id
        GROUP BY posts.created_at
        ORDER BY posts.created_at DESC;
        '''
        results = connectToMySQL('dojo_wall').query_db(query)

        all_posts = []

        if results:
            for row in results:
                # create an instance of user for each post
                one_post = cls(row)

                # collect the user data from the row in each iteration
                creator_data = {
                    'id' : row.get('users.id'),
                    'first_name' : row.get('first_name'),
                    'last_name' : row.get('last_name'),
                    'email' : row.get('email'),
                    'password' : row.get('password'),
                    'created_at' : row.get('created_at'),
                    'updated_at' : row.get('updated_at')
                }

                comment_data = {
                    'id' : row.get('comments.id'),
                    'user_id' : row.get('comments.user_id'),
                    'post_id' : row.get('comments.post_id'),
                    'content' : row.get('comments.content'),
                    'created_at' : row.get('comments.created_at'),
                    'updated_at' : row.get('comments.updated_at')
                }

                comment_creator_data = {
                    'id' : row.get('comment_creator.id'),
                    'first_name' : row.get('comment_creator.first_name'),
                    'last_name' : row.get('comment_creator.last_name'),
                    'email' : row.get('comment_creator.email'),
                    'password' : row.get('comment_creator.password'),
                    'created_at' : row.get('comment_creator.created_at'),
                    'updated_at' : row.get('comment_creator.updated_at')
                }

                print(f'Creator data: {creator_data}..............................................')
                print(f'Comment data: {comment_data}..............................................')
                print(f'Comment Creator data: {comment_creator_data}..............................................')

                one_creator = user.User(creator_data)

                one_post.creator = one_creator

                one_comment = comment.Comment(comment_data)

                one_comment.creator = user.User(comment_creator_data)

                one_post.comments.append(one_comment)

                all_posts.append(one_post)
        else:
            print('WHOOOPS! MY FOLLY')
        
        return all_posts