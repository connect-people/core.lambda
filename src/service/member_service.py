from .. import db
from ..model.member import Member
from ..model.token import Token
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def check_duplicate_by_login_id(login_id) -> bool:
    try:
        if Member.query.filter_by(login_id=login_id).first():
            return False
        return True

    except Exception as e:
        print(str(e))
        return False

    finally:
        db.session.close()


def signup(data) -> int:
    try:
        new_member = Member(
            login_id=data['login_id'],
            password=data['password'],
            name=data['name'],
            phone=data['phone']
        )
        save(new_member)
        return new_member.id

    except Exception as e:
        print(str(e))

    finally:
        db.session.close()


def signin(data) -> Member:
    try:
        return Member.query.filter_by(
            login_id=data['login_id'],
            password=data['password']
        ).first()

    except Exception as e:
        print(str(e))

    finally:
        db.session.close()


def token_generate_by_member_id(member_id) -> str:
    try:
        token = Serializer('cplab', expires_in=0).dumps({'member_id': member_id})
        new_token = Token(
            member_id=member_id,
            token=token
        )
        save(new_token)
        return new_token.token

    except Exception as e:
        print(str(e))

    finally:
        db.session.close()


def get_token_by_member_id(member_id) -> Token:
    try:
        return Token.query.filter_by(member_id=member_id).first().token

    except Exception as e:
        print(str(e))

    finally:
        db.session.close()


def get_member_by_token(token) -> Member:
    try:
        member_id = Token.query.filter_by(token=token).first().member_id
        db.session.close()
        return Member.query.filter_by(id=int(member_id)).first()

    except Exception as e:
        print(str(e))

    finally:
        db.session.close()


def save(data) -> None:
    db.session.add(data)
    db.session.commit()
