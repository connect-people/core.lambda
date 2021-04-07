from flask import request
from flask_restplus import Resource

from ..util.dto import MemberDto
from ..service.member_service import (
    signup,
    signin,
    get_token_by_member_id,
    token_generate_by_member_id,
    check_duplicate_by_login_id,
    get_member_by_token
)

api = MemberDto.api
_member_signup = MemberDto.member_signup
_member_signin = MemberDto.member_signin
_me = MemberDto.me

@api.route('/signup')
class Signup(Resource):
    @api.response(200, 'token')
    @api.response(401, '사용할 수 없는 아이디 입니다')
    @api.doc('회원 가입')
    @api.expect(_member_signup, validate=True)
    def post(self) -> (dict, int):
        """회원 가입"""
        data = request.json

        if check_duplicate_by_login_id(data['login_id']) is False:
            return {
                'error': '사용할 수 없는 아이디 입니다'
            }, 401

        member_id = signup(data=data)
        new_token = token_generate_by_member_id(member_id)
        return {
            'result': {
                'code': 1,
                'message': 'ok'
            },
            'data': {
                'token': new_token
            },
        }, 200


@api.route('/signin')
class Signin(Resource):
    @api.response(200, 'token')
    @api.response(401, '아이디 또는 패스워드를 다시 확인해 주세요')
    @api.doc('로그인')
    @api.expect(_member_signin, validate=True)
    def post(self) -> (dict, int):
        """회원 로그인"""
        data = request.json
        member = signin(data)
        if not member:
            return {
                'error': '아이디 또는 패스워드를 다시 확인해 주세요'
            }, 401
        token = get_token_by_member_id(member.id)
        return {
            'result': {
                'code': 1,
                'message': 'ok'
            },
            'data': {
                'token': token
            },
        }, 200


@api.route('/me')
class Me(Resource):
    @api.response(200, 'token')
    @api.response(401, '로그인이 필요합니다')
    @api.response(402, '회원 정보가 존재하지 않습니다')
    @api.doc('내 정보 조회')
    @api.header('token')
    @api.marshal_with(_me)
    def get(self):
        """내 정보 조회"""
        token = request.headers.get('token')
        if not token:
            return {
                'error': '로그인이 필요합니다'
            }, 401
        return {
            'result': {'code': 1, 'message': 'ok'},
            'data': get_member_by_token(token),
        }, 200
