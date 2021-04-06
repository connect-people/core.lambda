from flask import request
from flask_restplus import Resource

from ..util.dto import MemberDto
from ..service.member_service import (
    signup,
    signin,
    get_token_by_member_id,
    token_generate_by_member_id
)

api = MemberDto.api
_member_signup = MemberDto.member_signup
_member_signin = MemberDto.member_signin


@api.route('/signup')
class Signup(Resource):
    @api.response(200, 'token')
    @api.doc('회원 가입')
    @api.expect(_member_signup, validate=True)
    def post(self) -> (dict, int):
        """회원 가입"""
        data = request.json
        member_id = signup(data=data)
        new_token = token_generate_by_member_id(member_id)
        return {
            'token': new_token
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
            'token': token
        }, 200
