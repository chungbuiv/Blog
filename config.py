from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gotit:secret@localhost/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '154877121995661',
        'secret': 'dc28e22732c086384170a9885209a3b9'
    },
    'google': {
        'id': '104837107109-og80nseekntg7bfku0vdh2qtirgao0hk.apps.googleusercontent.com',
        'secret': 'SgRGPDTE-VmnsCrrfGMkskZH'
    }
}

db = SQLAlchemy(app)
from models.user import User
from models.post import Post
from models.action import Action
db.create_all()
db.session.commit()

# Length of content in brief
CONTENT_LENGTH = 5
