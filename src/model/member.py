from .. import db
from datetime import datetime


class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    password = db.Column(db.VARCHAR(255), nullable=False)
    name = db.Column(db.VARCHAR(100), nullable=False)
    login_id = db.Column(db.VARCHAR(100), nullable=False)
    phone = db.Column(db.VARCHAR(100))
    is_auth = db.Column(db.SMALLINT, default=0, nullable=False)
    created = db.Column(db.DATETIME, default="{:%Y-%m-%d %H:%I:%S}".format(datetime.now()), nullable=False)

