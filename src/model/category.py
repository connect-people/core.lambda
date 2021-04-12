from .. import db


class CategoryScope(db.Model):
    __tablename__ = "CategoryScope"

    ID = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    categoryID = db.Column(db.BIGINT)
    type = db.Column(db.INT, nullable=False)
    value = db.Column(db.VARCHAR(100), nullable=False)
