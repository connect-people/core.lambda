import logging

from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import BoardDto
from ..service.board_service import (
    save_new_board,
    get_all_boards,
    get_by_board_id,
    get_by_member_id,
    get_by_brand_name,
    upload_image
)
from ..service.member_service import get_member_by_token

api = BoardDto.api
_board = BoardDto.board
_board_save = BoardDto.board_save
_board_data = BoardDto.board_data
_board_detail = BoardDto.board_detail
_board_search = BoardDto.board_search

arguments = reqparse.RequestParser()
arguments.add_argument('page', type=int, required=False, default=1, help='현재 페이지')
arguments.add_argument('per_page', type=int, required=False, default=200, help='한 페이지에 보여질 갯수')


@api.route('/')
class Board(Resource):
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
    @api.header('token')
    @api.expect(_board_save, validate=True)
    def post(self):
        """게시판 등록"""
        token = request.headers.get('token')
        data = request.json

        if not token or token == 'null':
            api.abort(401, '로그인이 필요합니다')

        member = get_member_by_token(token)
        if not member:
            api.abort(401, '회원정보를 찾을 수가 없습니다')

        return save_new_board(data=data, member_id=member.id), 200


@api.route('/images')
class BoardImage(Resource):
    @api.response(200, 'ok')
    @api.response(401, 'file not exist')
    @api.doc('이미지 임시 업로드')
    def post(self):
        """이미지 임시 업로드"""
        file = request.files.get('tempFile')
        if not file:
            api.abort(401, 'file not exist')

        return_url = upload_image(file)

        return {'data': {'returnUrl': return_url}}, 200


@api.route('/<int:board_id>')
@api.param('board_id', 'board_id')
class BoardDetail(Resource):
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
                logging.debug(token)
                raise Exception(404, '회원정보를 찾을 수가 없습니다')

            board = get_by_board_id(board_id)

            if not board:
                raise Exception(403, '게시글을 찾을 수 없습니다')

            return {'data': board}, 200

        except Exception as e:
            logging.error(e)
            api.abort(e.args[0], e.args[1])


@api.route('/me')
class MyBoard(Resource):
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

            logging.debug(token)
            logging.debug(member.id)

            board = get_by_member_id(member.id, page, per_page)

            if not board:
                raise Exception(403, '게시글을 찾을 수 없습니다')

            return board

        except Exception as e:
            logging.error(str(e))
            api.abort(e.args[0], e.args[1])


@api.route('/search-brand')
class Board(Resource):
    @api.doc('브랜드 검색')
    @api.expect(arguments)
    @api.marshal_list_with(_board_search)
    def post(self):
        """브랜드 검색"""
        args = arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 200)
        token = request.headers.get('token')
        data = request.json
        boards = get_by_brand_name(data.get('keyword'), page, per_page)
        return {
            'result': {
                'code': 1,
                'message': 'ok'
            },
            'data': boards['items'],
            'page': page,
            'pages': boards['pages'],
            'per_page': per_page,
            'total': boards['total']
        }, 200