from .. import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime


class Board(db.Model):
    __tablename__ = "Board"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brandName = db.Column(db.String(100))
    memberID = db.Column(db.BIGINT)
    title = db.Column(db.String(100))
    subTitle = db.Column(db.String(100))
    content = db.Column(db.String(64000))
    majorCategoryID = db.Column(db.Integer)
    created = db.Column(db.DateTime, default="{:%Y-%m-%d %H:%I:%S}".format(datetime.now()), nullable=False)
    boardImage = relationship("BoardImage")


class BoardImage(db.Model):
    __tablename__ = "BoardImage"

    ID = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    boardID = db.Column(db.BIGINT, ForeignKey("Board.ID"))
    imageNumber = db.Column(db.INT)
    imageUrl = db.Column(db.VARCHAR(500))
    created = db.Column(db.DATETIME, default="{:%Y-%m-%d %H:%I:%S}".format(datetime.now()), nullable=False)
