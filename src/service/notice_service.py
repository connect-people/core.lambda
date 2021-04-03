from .. import db
from ..model.notice import Notice
from datetime import datetime
from sqlalchemy import desc
from flask_sqlalchemy import Pagination


def save_new_notice(data) -> (dict, int):
    new_notice = Notice(
        title=data['title'],
        content=data['content'],
        login_id=data['login_id'],
        member_name=data['member_name'],
        created=data["created"] if 'created' in data else "{:%Y-%m-%d %H:%I:%S}".format(datetime.now()),
    )
    save(new_notice)
    response_object = {
        'code': 1,
        'message': 'ok'
    }
    return response_object, 200


def get_all_notices() -> list:
    return Notice.query.order_by(desc(Notice.id)).all().Pagination(1, 20, error_out=False)


def get_by_notice_id(notice_id) -> dict:
    return Notice.query.filter_by(id=notice_id).first()


def save(data):
    db.session.add(data)
    db.session.commit()
