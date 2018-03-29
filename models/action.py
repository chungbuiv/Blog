from datetime import datetime
from models.base import db, ModelMethods


class Action(db.Model, ModelMethods):
    _table_name = 'action'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    time = db.Column(db.DateTime())

    def __init__(self, post_id, user_id, like_time=None):
        self.post_id = post_id
        self.user_id = user_id

        if like_time:
            self.time = like_time
        else:
            self.time = datetime.now()

    def __repr__(self):
        return "Like: {} {} {}".format(self.post_id, self.user_id, self.time)
