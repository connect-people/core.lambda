from .. import db
from datetime import datetime


class Token(db.Model):
    __tablename__ = "token"

    member_id = db.Column(db.BIGINT, primary_key=True, nullable=False)
    token = db.Column(db.VARCHAR(100), nullable=False)
    created = db.Column(db.DATETIME, default="{:%Y-%m-%d %H:%I:%S}".format(datetime.now()), nullable=False)

