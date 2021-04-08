from .. import db
from datetime import datetime


class Notice(db.Model):
    __tablename__ = "notice"

    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    title = db.Column(db.VARCHAR(50))
    member_id = db.Column(db.BIGINT, nullable=False)
    login_id = db.Column(db.VARCHAR(100))
    content = db.Column(db.VARCHAR(64000))
    member_name = db.Column(db.VARCHAR(50))
    created = db.Column(db.DATETIME, default="{:%Y-%m-%d %H:%I:%S}".format(datetime.now()), nullable=False)
