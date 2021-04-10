from .. import db
from ..model.board import Board
from sqlalchemy.sql import desc, text
import logging as log


def save_new_board(data) -> int:
    try:
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
        return new_notice.ID
    except Exception as e:
        log.error(str(e))
    finally:
        db.session.close()


def get_all_boards(page=1, per_page=200):
    try:
        count = db.engine.execute(text(
            """
            SELECT COUNT(*) FROM Board
            """
        )).scalar()

        query = db.engine.execute(text(
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
            LIMIT :per_page OFFSET :page
            """), per_page=per_page, page=page
        )

        return {
            'items': query.all(),
            'page': page,
            'pages': (count // per_page) + (1 if (count / per_page) > 0 else 0),
            'per_page': per_page,
            'total': count
        }
    except Exception as e:
        log.error(str(e))
    finally:
        db.session.close()


def get_by_board_id(notice_id) -> dict:
    try:
        board = Board.query.filter_by(ID=notice_id).first()

        board_images = db.engine.execute(text(
            """
            SELECT
                imageUrl AS imageUrl
            FROM BoardImage
            WHERE boardID = :board_id
            ORDER BY imageNumber ASC
            """), board_id=board.ID
        ).all()

        board.imageUrls = [bi[0] for bi in board_images]

        return board
    except Exception as e:
        log.error(str(e))
    finally:
        db.session.close()


def get_by_member_id(member_id, page=1, per_page=20) -> Board:
    try:
        count = db.engine.execute(text(
            """
            SELECT COUNT(*) FROM Board
            """
        )).scalar()

        boards = db.engine.execute(text(
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
            WHERE b.memberID = :member_id
            ORDER BY b.created DESC
            LIMIT :per_page OFFSET :page
            """), member_id=member_id, per_page=per_page, page=page
        ).all()

        return {
            'items': boards,
            'page': page,
            'pages': (count // per_page) + (1 if (count / per_page) > 0 else 0),
            'per_page': per_page,
            'total': count
        }
    except Exception as e:
        log.error(str(e))
    finally:
        db.session.close()
        pass


def save(data):
    db.session.add(data)
    db.session.commit()
