import json
from flask import jsonify
from flask_restful import Resource
from flask_login import login_required, current_user

from models.post import Post
from models.action import Action


class ActionApi(Resource):

    @login_required
    def get(self, post_id):
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

        users = Post.get_user_liked(post_id=post_id)
        res = {post_id: {
            'users': users
        }}
        return json.dumps(res)

    @login_required
    def post(self, post_id):
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

        user_id = current_user.id
        action = Action.query.filter_by(post_id=post_id, user_id=user_id).all()
        print(action)
        if len(action) == 0:
            like = Action(post_id=post_id, user_id=user_id)
            like.save()
        res = {post_id: dict(user_id=user_id)}
        return json.dumps(res)
