from datetime import datetime

from sqlalchemy import text

from models.base import db, ModelMethods


class Post(db.Model, ModelMethods):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    time = db.Column(db.DateTime())

    def __init__(self, title, content, user_id, time=None):
        self.title = title
        self.content = content
        self.user_id = user_id
        if time is None:
            self.time = datetime.now()
        else:
            self.time = time

    @classmethod
    def get_user_liked(cls, post_id):
        sql=text('select user.name from action join user on action.user_id = user.id where action.post_id = :post_id')
        result=db.engine.execute(sql,post_id=post_id)
        names=[]
        for row in result:
            names.append(row[0])
        return names

    def __repr__(self):
        return "Post: {} {} {} {}".format(self.title, self.content, self.user_id, self.time)
