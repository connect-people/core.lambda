from flask import request
from flask_restplus import Resource, reqparse

from ..util.response import Response
from ..util.dto import BoardDto
from ..service.board_service import (
    save_new_board,
    get_all_boards,
    get_by_board_id,
    get_by_member_id
)
from ..service.member_service import get_member_by_token

import pprint
import logging

api = BoardDto.api
_board = BoardDto.board
_board_detail = BoardDto.board_detail

resp = Response()

pp = pprint.PrettyPrinter(indent=4)


arguments = reqparse.RequestParser()
arguments.add_argument('page', type=int, required=False, default=1, help='현재 페이지')
arguments.add_argument('per_page', type=int, required=False, default=20, help='한 페이지에 보여질 갯수')


@api.route('/')
class BoardList(Resource):
    @api.doc('게시글 전체 리스트')
    # @api.marshal_list_with(_board, envelope='data')
    @api.expect(arguments)
    @api.marshal_list_with(_board)
    def get(self):
        """게시판 전체 리스트"""
        args = arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 200)
        return get_all_boards(page, per_page)

    @api.response(200, 'ok')
    @api.doc('게시판 등록')
    @api.expect(_board, validate=True)
    def post(self):
        """게시판 등록"""
        data = request.json
        return save_new_board(data=data)


@api.route('/<int:board_id>')
@api.param('board_id', 'board_id')
class Notice(Resource):
    @api.doc('게시판 상세')
    @api.header('token')
    @api.response(200, 'ok')
    @api.response(401, '로그인이 필요합니다')
    @api.response(403, '게시글을 찾을 수 없습니다')
    @api.marshal_with(_board_detail)
    def get(self, board_id) -> dict:
        """게시글 상세"""
        try:
            token = request.headers.get('token')

            if not token or token == 'null':
                raise Exception(401, '로그인이 필요합니다')

            if not get_member_by_token(token):
                raise Exception(404, '회원정보를 찾을 수가 없습니다')

            board = get_by_board_id(board_id)

            if not board:
                raise Exception(403, '게시글을 찾을 수 없습니다')

            resp.set_result(code=200, message='ok')
            resp.set_contents(data=board)

        except Exception as e:
            resp.set_result(code=e.args[0], message=e.args[1])

        finally:
            return resp.send()


@api.route('/me')
class Notice(Resource):
    @api.doc('내 작성글')
    @api.header('token')
    @api.response(200, 'ok')
    @api.response(401, '로그인이 필요합니다')
    @api.response(403, '게시글을 찾을 수 없습니다')
    @api.expect(arguments)
    @api.marshal_list_with(_board)
    def get(self):
        """내 작성글"""
        try:
            token = request.headers.get('token')
            args = arguments.parse_args(request)
            page = args.get('page', 1)
            per_page = args.get('per_page', 200)

            if not token or token == 'null':
                raise Exception(401, '로그인이 필요합니다')

            member = get_member_by_token(token)
            if not member:
                raise Exception(404, '회원정보를 찾을 수가 없습니다')

            print(member.id)
            print(member.login_id)

            board = get_by_member_id(member.id, page, per_page)

            if not board:
                raise Exception(403, '게시글을 찾을 수 없습니다')

            return board

        except Exception as e:
            logging.error(str(e))
