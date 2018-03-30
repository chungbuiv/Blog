import json

from flask import abort, jsonify
from flask_restful import Resource, reqparse
from flask_login import login_required, current_user

from models.post import Post
from models.user import User

from config import CONTENT_LENGTH


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
parser.add_argument('phone')
parser.add_argument('job', choices=('Student', 'Teacher', 'Other'), help='Bad choice: {error_msg}')


class UserApi(Resource):

    @login_required
    # @info_required
    def get(self, id=None):
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
            id = current_user.id

        posts = Post.query.filter_by(user_id=id)
        if not posts:
            abort(404)
        res = {}
        for post in posts:
            users = Post.get_user_liked(post.id)
            num_users = len(users)
            if num_users > 2:
                like = str(users[0])+', '+str(users[1])+' and '+(num_users-2)+' other people liked this post'
            elif num_users == 2:
                like = str(users[0])+', '+str(users[1])+' liked this post'
            elif num_users == 1:
                like = str(users[0])+' liked this post'
            else:
                like = None
            res[post.id] = {
                'title': post.title,
                'content': post.content[:CONTENT_LENGTH],
                'like': like
            }
        return json.dumps(res)

    @login_required
    def post(self):
        args = parser.parse_args()
        user_id = current_user.id
        # user_id = 1
        user = User.query.filter_by(id=user_id).first()
        print(user)
        user.name = args['name']
        # current_user.name = user.name
        if user.role:
            user.phone = args['phone']
            # current_user.phone = user.phone
            res = {user.id: {
                'name': user.name,
                'phone': user.phone
            }}
        else:
            user.job = args['job']
            # current_user.job = user.job
            res = {user.id: {
                'name': user.name,
                'job': user.job
            }}
        user.save()
        return json.dumps(res)
