from flask import request
from flask_restplus import Resource

from ..util.dto import BoardDto
from ..service.board_service import save_new_board, get_all_boards, get_by_board_id

api = BoardDto.api
_board = BoardDto.board


@api.route('/')
class BoardList(Resource):
    @api.doc('게시글 전체 리스트')
    @api.marshal_list_with(_board, envelope='data')
    def get(self):
        """게시판 전체 리스트"""
        return get_all_boards()

    @api.response(200, 'ok')
    @api.doc('게시판 등록')
    @api.expect(_board, validate=True)
    def post(self):
        """게시판 등록"""
        data = request.json
        return save_new_board(data=data)


@api.route('/<int:board_id>')
@api.param('board_id', 'board_id')
@api.response(404, 'notice not found')
class Notice(Resource):
    @api.doc('게시판 상세')
    @api.marshal_with(_board)
    def get(self, board_id) -> dict:
        """게시글 상세"""
        board = get_by_board_id(board_id)
        if not board:
            api.abort(404)
        else:
            return board