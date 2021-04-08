from .. import db
from ..model.notice import Notice
from datetime import datetime
from sqlalchemy import desc
import logging as log


def save_new_notice(data) -> (dict, int):
    try:
        new_notice = Notice(
            title=data['title'],
            content=data['content'],
            login_id=data['login_id'],
            member_id=data['member_id'],
            member_name=data['member_name']
        )
        save(new_notice)
        return {"notice_id": new_notice.id}, 200

    except Exception as e:
        log.error(str(e))

    finally:
        db.session.close()


def get_all_notices(page=1, per_page=20) -> Notice:
    try:
        # return Notice.query.order_by(desc(Notice.id)).all()
        return Notice.query.order_by(desc(Notice.id)).paginate(page=page, per_page=per_page)

    except Exception as e:
        log.error(str(e))

    finally:
        db.session.close()


def get_by_notice_id(notice_id) -> Notice:
    try:
        return Notice.query.filter_by(id=notice_id).first()

    except Exception as e:
        log.error(str(e))

    finally:
        db.session.close()


def delete_by_notice_id(notice_id) -> Notice:
    try:
        return Notice.query.filter_by(id=notice_id).delete()

    except Exception as e:
        log.error(str(e))

    finally:
        db.session.close()


def save(data):
    db.session.add(data)
    db.session.commit()
