from .. import db
from ..model.member import Member
from ..model.token import Token
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def signup(data) -> int:
    new_member = Member(
        login_id=data['login_id'],
        password=data['password'],
        name=data['name'],
        phone=data['phone']
    )
    save(new_member)
    return new_member.id


def signin(data) -> Member:
    return Member.query.filter_by(
        login_id=data['login_id'],
        password=data['password']
    ).first()


def token_generate_by_member_id(member_id) -> str:
    token = Serializer('cplab', expires_in=0).dumps({'member_id': member_id})
    new_token = Token(
        member_id=member_id,
        token=token
    )
    save(new_token)
    return new_token.token


def get_token_by_member_id(member_id) -> Token:
    return Token.query.filter_by(member_id=member_id).first().token


def save(data) -> None:
    db.session.add(data)
    db.session.commit()
