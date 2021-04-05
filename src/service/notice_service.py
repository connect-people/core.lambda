from .. import db
from ..model.notice import Notice
from datetime import datetime
from sqlalchemy import desc


def save_new_notice(data) -> (dict, int):
    new_notice = Notice(
        title=data['title'],
        content=data['content'],
        login_id=data['login_id'],
        member_name=data['member_name'],
        created=data["created"] if 'created' in data else "{:%Y-%m-%d %H:%I:%S}".format(datetime.now()),
    )
    save(new_notice)
    return {"notice_id": new_notice.id}, 200


def get_all_notices(page=1, per_page=20) -> list:
    # return Notice.query.order_by(desc(Notice.id)).all()
    return Notice.query.order_by(desc(Notice.id)).paginate(page=page, per_page=per_page)


def get_by_notice_id(notice_id) -> dict:
    return Notice.query.filter_by(id=notice_id).first()


def delete_by_notice_id(notice_id):
    return Notice.query.filter_by(id=notice_id).delete()


def save(data):
    db.session.add(data)
    db.session.commit()
