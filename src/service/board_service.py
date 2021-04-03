from .. import db
from ..model.board import Board
from sqlalchemy.sql import select, func


def save_new_board(data) -> (dict, int):
    new_notice = Board(
        brandName=data['brandName'],
        memberID=data['memberID'],
        title=data['title'],
        subTitle=data['subTitle'],
        content=data['content'],
        majorCategoryID=data['majorCategoryID'],
        created=data['created']
    )
    save(new_notice)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return response_object, 200


def get_all_boards() -> list:
    query = db.engine.execute(
        """
        SELECT
        b.ID AS ID, 
        b.brandName AS brandName, 
        b.memberID AS memberID, 
        b.title AS title, 
        b.subTitle AS subTitle, 
        b.content AS content, 
        IFNULL((SELECT bi.imageUrl FROM BoardImage bi WHERE bi.boardID = b.ID AND bi.imageNumber = 0 LIMIT 1), null) AS imageUrl, 
        IFNULL((SELECT c.name FROM Category AS c WHERE c.ID = b.majorCategoryID), null) AS majorCategoryName, 
        b.created AS created 
        FROM Board AS b 
        ORDER BY b.created DESC
        """
    )
    return query.all()


def get_by_board_id(notice_id) -> dict:
    return Board.query.filter_by(id=notice_id).first()


def save(data):
    db.session.add(data)
    db.session.commit()
