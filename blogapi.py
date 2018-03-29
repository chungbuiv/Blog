from flask import jsonify
from flask_restful import Api
from flask_login import LoginManager, login_user, logout_user, current_user

from config import app
from common.oauth import OAuthSignIn
from resources.user import UserApi
from resources.post import PostApi
from resources.action import ActionApi
from models.user import User


api = Api(app)
api.add_resource(UserApi, '/user/', '/user/<int:id>/')
api.add_resource(PostApi, '/post/', '/post/<int:id>/', '/post/<int:id>/<int:page>/')
api.add_resource(ActionApi, '/like/<int:post_id>')



####################################################################################

lm = LoginManager(app)
lm.login_view = 'login'


@lm.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/')
@app.route('/home')
def home():
    return jsonify({
        'message': 'Welcome to GotIt Blog!'
    })


@app.route('/logout')
def logout():
    email = None if current_user.is_anonymous else current_user.email
    logout_user()
    return jsonify(dict(email=email,status='0',message='Logout successfully!'))


@app.route('/login/<provider>')
@app.route('/register/<provider>')
@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return jsonify(dict(email=current_user.email,status='1',message='User already logged in!'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


# Handle Facebook/Google callback
@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return jsonify(dict(email=current_user.email,status='1',message='User already logged in!'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, email, role = oauth.callback()
    if social_id is None:
        return jsonify(dict(email=email,status='0',message='Authentication failed!'))
    user = User.query.filter_by(email=email).first()
    if user:
        if bool(user.role) != bool(role):
            user_type = 'Facebook' if user.role else 'Google'
            return jsonify({
                'message': user.email + ' is ' + user_type + ' account. Please login by ' + user_type
            })
    else:
        user = User(email=email, role=role)
        user.save()
    login_user(user, True)
    return jsonify(dict(email=current_user.email,status='1',message='Login successfully!'))

####################################################################################


if __name__ == '__main__':
    app.run(debug=True)
