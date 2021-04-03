from .. import db


class Notice(db.Model):
    __tablename__ = "notice"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    login_id = db.Column(db.String(100))
    content = db.Column(db.String(64000))
    member_name = db.Column(db.String(50))
    created = db.Column(db.DateTime, nullable=False)
