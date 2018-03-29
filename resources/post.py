import json
from flask import jsonify
from flask_restful import Resource, abort, reqparse
from flask_login import current_user, login_required

from models.post import Post
from config import CONTENT_LENGTH

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help="Title cannot be blank!")
parser.add_argument('content', type=str, required=True, help="Content cannot be blank!")


class PostApi(Resource):

    # @login_required
    # @info_required
    def get(self, id=None, page=1):
        # Check user information before processing
        if current_user.role:
            if not current_user.name or not current_user.phone:
                return jsonify({
                    'message': 'Name and phone number are required!'
                })
        else:
            if not current_user.name or not current_user.job:
                return jsonify({
                    'message': 'Name and job information are required!'
                })

        if id is None:
            posts = Post.query.paginate(page, 10).items
        else:
            posts = Post.query.filter_by(id=id)
        if not posts:
            abort(404)
        res = {}
        for post in posts:
            users = Post.get_user_liked(post.id)
            print(users)
            num_users = len(users)
            if num_users > 2:
                like = str(users[0]) + ', ' + str(users[1]) + ' and ' + str(num_users - 2) + \
                       ' other people liked this post'
            elif num_users == 2:
                like = str(users[0]) + ', ' + str(users[1]) + ' liked this post'
            elif num_users == 1:
                like = str(users[0]) + ' liked this post'
            else:
                like = None
            if id is None:
                res[post.id] = {
                    'title': post.title,
                    'content': post.content[:CONTENT_LENGTH],
                    'like': like
                }
            else:
                res[post.id] = {
                    'title': post.title,
                    'content': post.content,
                    'like': like
                }
        return json.dumps(res)

    # @login_required
    # @info_required
    def post(self):
        # Check user information before processing
        if current_user.role:
            if not current_user.name or not current_user.phone:
                return jsonify({
                    'message': 'Name and phone number are required!'
                })
        else:
            if not current_user.name or not current_user.job:
                return jsonify({
                    'message': 'Name and job information are required!'
                })

        args = parser.parse_args()
        title = args['title']
        content = args['content']
        user_id = current_user.id
        post = Post(title, content, user_id)
        post.save()
        res = {post.id: {
            'title': post.title,
            'content': post.content,
            'user_id': user_id
        }}
        return json.dumps(res)
